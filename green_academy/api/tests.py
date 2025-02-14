from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from api.models import Course, Enrollment


### Model Tests ###
class CourseModelTest(TestCase):
    def setUp(self):
        """Create a test course."""
        self.course = Course.objects.create(
            title="Introduction to Sustainability",
            description="Learn about environmental conservation.",
            instructor="Dr. Green",
            start_date="2024-01-01",
            end_date="2024-06-01"
        )

    def test_course_creation(self):
        """Test if the course is created correctly"""
        self.assertEqual(self.course.title, "Introduction to Sustainability")
        self.assertEqual(self.course.instructor, "Dr. Green")


class EnrollmentModelTest(TestCase):
    def setUp(self):
        """Create a test enrollment."""
        self.course = Course.objects.create(
            title="Advanced Climate Change",
            description="Deep dive into climate change solutions.",
            instructor="Prof. Blue",
            start_date="2024-02-01",
            end_date="2024-07-01"
        )
        self.enrollment = Enrollment.objects.create(
            student_id="12345",
            student_name="Alice Johnson",
            student_email="alice@example.com",
            course=self.course
        )

    def test_enrollment_creation(self):
        """Test if a student can enroll in a course"""
        self.assertEqual(self.enrollment.student_name, "Alice Johnson")
        self.assertEqual(self.enrollment.course.title, "Advanced Climate Change")


### API Tests ###
class CourseAPITest(APITestCase):
    def setUp(self):
        """Create a test staff user and authenticate requests."""
        self.user = User.objects.create_user(username="testuser", password="password123", is_staff=True)  # ✅ Make user staff
        self.client.force_authenticate(user=self.user) 

        self.course = Course.objects.create(
            title="Sustainability 101",
            description="Introduction to environmental sustainability.",
            instructor="Dr. Jane Doe",
            start_date="2024-01-01",
            end_date="2024-06-01"
        )

    def test_get_courses(self):
        """Test retrieving the list of courses."""
        response = self.client.get("/api/courses/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_course(self):
        """Test creating a new course."""
        data = {
            "title": "Climate Change",
            "description": "Advanced discussions on climate change.",
            "instructor": "Dr. John Smith",
            "start_date": "2024-03-01",
            "end_date": "2024-09-01"
        }
        response = self.client.post("/api/courses/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)


class EnrollmentAPITest(APITestCase):
    def setUp(self):
        """Create a test staff user and authenticate requests."""
        self.user = User.objects.create_user(username="testuser", password="password123", is_staff=True)  # ✅ Make user staff
        self.client.force_authenticate(user=self.user)  

        self.course = Course.objects.create(
            title="Renewable Energy",
            description="Exploring alternative energy sources.",
            instructor="Prof. Green",
            start_date="2024-02-01",
            end_date="2024-07-01"
        )
        self.enrollment = Enrollment.objects.create(
            student_id="001",
            student_name="Alice Johnson",
            student_email="alice@example.com",
            course=self.course
        )

    def test_get_enrollments(self):
        """Test retrieving the list of enrollments."""
        response = self.client.get("/api/enrollments/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_enrollment(self):
        """Test creating a new enrollment."""
        data = {
            "student_id": "002",
            "student_name": "Bob Smith",
            "student_email": "bob@example.com",
            "course": self.course.title  # Assuming the API uses course title for enrollment
        }
        response = self.client.post("/api/enrollments/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Enrollment.objects.count(), 2)
