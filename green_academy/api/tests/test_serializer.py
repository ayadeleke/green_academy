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
            "student_id": "00001",
            "student_name": "Test Student",
            "student_email": "student@example.com",
            "course": self.course.title,  # SlugRelatedField requires title
            "enrollment_date": date(2025, 2, 1),
        }

    def test_valid_enrollment_serializer(self):
        """Ensure valid enrollment data passes serializer validation."""
        serializer = EnrollmentSerializer(data=self.enrollment_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_invalid_enrollment_serializer(self):
        """Ensure invalid email raises validation error."""
        self.enrollment_data["student_email"] = "invalid-email"
        serializer = EnrollmentSerializer(data=self.enrollment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("student_email", serializer.errors)
        self.assertIn("Enter a valid email address.", serializer.errors["student_email"][0])

    def test_duplicate_enrollment(self):
        """Ensure duplicate enrollment is not allowed."""
        Enrollment.objects.create(
            student_id=self.enrollment_data["student_id"],
            student_name=self.enrollment_data["student_name"],
            student_email=self.enrollment_data["student_email"],
            course=self.course,
            enrollment_date=self.enrollment_data["enrollment_date"],
        )

        # Try to enroll the same student again
        serializer = EnrollmentSerializer(data=self.enrollment_data)
        self.assertFalse(serializer.is_valid())

        # Assert the actual error message
        self.assertIn("non_field_errors", serializer.errors)
        self.assertIn("The fields student_id, course must make a unique set.", serializer.errors["non_field_errors"][0])



