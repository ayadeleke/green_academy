from django.test import TestCase
from api.models import Course, Enrollment
from api.serializers import CourseSerializer, EnrollmentSerializer
from datetime import date

class CourseSerializerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Sample Course",
            description="Sample course description",
            instructor="Dr. Jane Doe",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
        )
        self.course_data = {
            "title": "New Course",
            "description": "Another course",
            "instructor": "Dr. John Smith",
            "start_date": date(2025, 3, 1),
            "end_date": date(2025, 10, 1),
        }

    def test_valid_course_serializer(self):
        serializer = CourseSerializer(data=self.course_data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_course_serializer(self):
        self.course_data["end_date"] = date(2024, 1, 1)  # End date before start date
        serializer = CourseSerializer(data=self.course_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("End date must be later than start date", str(serializer.errors))

    def test_duplicate_course_title(self):
        duplicate_course_data = {
            "title": "Sample Course",  # Same as existing course
            "description": "Duplicate title test",
            "instructor": "Dr. New Instructor",
            "start_date": date(2025, 5, 1),
            "end_date": date(2025, 11, 1),
        }
        serializer = CourseSerializer(data=duplicate_course_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("A course with this title already exists", str(serializer.errors))

    def test_duplicate_course_by_same_instructor(self):
        duplicate_course_data = {
            "title": "Sample Course",
            "description": "Same instructor duplicate",
            "instructor": "Dr. Jane Doe",  # Same instructor as existing course
            "start_date": date(2025, 5, 1),
            "end_date": date(2025, 11, 1),
        }
        serializer = CourseSerializer(data=duplicate_course_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("This instructor already has a course with this title", str(serializer.errors))


class EnrollmentSerializerTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Sample Course",
            description="Sample course description",
            instructor="Dr. Jane Doe",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
        )

        self.enrollment_data = {
            "student_id": 1,
            "student_name": "Test Student",
            "student_email": "student@example.com",
            "course": self.course.title,  # Use title, since serializer uses SlugRelatedField
            "enrollment_date": date(2025, 2, 1),
        }

    def test_valid_enrollment_serializer(self):
        serializer = EnrollmentSerializer(data=self.enrollment_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_enrollment_serializer(self):
        self.enrollment_data["student_email"] = "invalid-email"
        serializer = EnrollmentSerializer(data=self.enrollment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("Enter a valid email address.", str(serializer.errors))

    def test_duplicate_enrollment(self):
        # Create an enrollment in the database
        Enrollment.objects.create(
            student_id=1,
            student_name="Test Student",
            student_email="student@example.com",
            course=self.course,
            enrollment_date=date(2025, 2, 1),
        )

        # Try to enroll the same student again
        serializer = EnrollmentSerializer(data=self.enrollment_data)
        self.assertFalse(serializer.is_valid())

        # Assert the actual error message
        self.assertIn('student_id', str(serializer.errors))
        self.assertIn('course', str(serializer.errors))
        self.assertIn("unique", str(serializer.errors))


