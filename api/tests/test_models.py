from django.test import TestCase
from api.models import Course, Enrollment, UserProfile
from django.contrib.auth import get_user_model
from datetime import date
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError

User = get_user_model()

class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            description="A sample course for testing",
            instructor="Dr. John Doe",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
        )

    def test_course_creation(self):
        self.assertEqual(self.course.title, "Test Course")
        self.assertEqual(self.course.instructor, "Dr. John Doe")

    def test_course_end_date_validation(self):
        course = Course(
            title="Invalid Course",
            description="Invalid",
            instructor="Dr. Jane Doe",
            start_date=date(2025, 12, 31),
            end_date=date(2025, 1, 1),
        )
        with self.assertRaises(ValidationError):
            course.full_clean()  # This calls the `clean()` method

    def test_course_str_representation(self):
        self.assertEqual(str(self.course), "Test Course")


class EnrollmentModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Test Course",
            description="Sample description",
            instructor="Dr. John Doe",
            start_date=date(2025, 1, 1),
            end_date=date(2025, 12, 31),
        )
        self.student = User.objects.create_user(username="student1", email="student@example.com", password="test1234")
        self.enrollment = Enrollment.objects.create(
            student_id=self.student.id,
            student_name="Student One",
            student_email=self.student.email,
            course=self.course,
        )

    def test_enrollment_creation(self):
        self.assertEqual(self.enrollment.student_name, "Student One")
        self.assertEqual(self.enrollment.course.title, "Test Course")

    def test_duplicate_enrollment(self):
        with self.assertRaises(Exception):
            Enrollment.objects.create(
                student_id=self.student.id,
                student_name="Student One",
                student_email=self.student.email,
                course=self.course,
            )

    def test_enrollment_str_representation(self):
        self.assertEqual(
            str(self.enrollment),
            f"Student One ({self.student.id}) - Test Course"
        )


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", email="test@example.com", password="password123")
        # Ensure there is no existing UserProfile, just in case
        UserProfile.objects.filter(user=self.user).delete()

    def test_user_profile_creation(self):
        """Ensures a UserProfile is created when a user is created."""
        try:
            # Create the profile
            profile = UserProfile.objects.create(user=self.user, role="student")
            self.assertEqual(profile.user.username, "testuser")
            self.assertEqual(profile.role, "student")
        except IntegrityError:
            self.fail("UserProfile creation failed due to unique constraint violation")

    def test_user_profile_update_role(self):
        """Test to update the role of an existing UserProfile"""
        profile = UserProfile.objects.create(user=self.user, role="student")
        # Update the role
        profile.role = "instructor"
        profile.save()
        self.assertEqual(profile.role, "instructor")

    def test_user_profile_str_representation(self):
        profile = UserProfile.objects.create(user=self.user, role="instructor")
        self.assertEqual(str(profile), "testuser - instructor")
        profile.role = "student"
        profile.save()
        self.assertEqual(str(profile), "testuser - student")