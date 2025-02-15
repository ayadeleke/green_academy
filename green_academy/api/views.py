from typing import Any, TYPE_CHECKING
from django.core.cache import cache
from django.db.models.query import QuerySet
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.vary import vary_on_cookie
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import SAFE_METHODS
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.serializers import BaseSerializer
from rest_framework.exceptions import APIException
from django.db import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from api.permissions import IsAdmin, IsInstructor, IsStudent, IsAdminOrInstructorOrReadOnly
from api.models import Course, Enrollment
from api.serializers import CourseSerializer, EnrollmentSerializer

if TYPE_CHECKING:
    from api.models import Course

# Pagination class for CourseViewSet
class CoursePagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

# Pagination class for EnrollmentViewSet
class EnrollmentPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Course ViewSet (Only Admins & Instructors Can Modify)
@method_decorator(csrf_exempt, name='dispatch')
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by("id")
    serializer_class = CourseSerializer
    pagination_class = CoursePagination

    def get_authentication_classes(self):
        if self.request.method in SAFE_METHODS:  # GET, HEAD, OPTIONS
            return [JWTAuthentication(), BasicAuthentication()]
        return [JWTAuthentication()]  # POST, PUT, DELETE (Admin/Instructor Only)

    # Permissions: Students can view, only Admin/Instructors can modify
    permission_classes = [IsAdminOrInstructorOrReadOnly]

    @swagger_auto_schema(
        operation_description="Retrieve all courses (Students can view with JWT or Basic Authentication)",
        responses={200: CourseSerializer(many=True)},
    )
    def list(self, request):
        """Retrieves all available courses."""
        return super().list(request)

    @swagger_auto_schema(
        operation_description="Create a new course (Admins/Instructors only)",
        responses={201: CourseSerializer()},

    )
    def perform_create(self, serializer):
        """Handles course creation with error handling."""
        try:
            serializer.save()
        except IntegrityError:
            raise APIException("A course with this title already exists.")

# Enrollment ViewSet (Admins & Instructors can filter by student_id & course_id)
class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    pagination_class = EnrollmentPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrInstructorOrReadOnly]

    def get_queryset(self):
        """
        Allow Admins & Instructors to filter enrollments by student_id and course_id.
        """
        queryset = Enrollment.objects.all().order_by("id")
        student_id = self.request.query_params.get("student_id")
        course_id = self.request.query_params.get("course_id")

        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        return queryset

    @swagger_auto_schema(
        operation_description="Retrieve all enrollments (Admins/Instructors only)",
        manual_parameters=[
            openapi.Parameter(
                'student_id',
                openapi.IN_QUERY,
                description="Filter enrollments by student ID",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'course_id',
                openapi.IN_QUERY,
                description="Filter enrollments by course ID",
                type=openapi.TYPE_STRING
            )
        ],
        responses={200: EnrollmentSerializer(many=True)}
    )
    def list(self, request):
        """Retrieves all enrollments with optional filtering."""
        return super().list(request)

    @swagger_auto_schema(
        operation_description="Enroll a student in a course (Admins/Instructors only)",
        responses={201: EnrollmentSerializer()},
    )
    def perform_create(self, serializer):
        """Handles enrollment creation with error handling."""
        try:
            serializer.save()
        except IntegrityError:
            raise APIException("This student is already enrolled in this course.")

# Student Enrollment ViewSet (Students can only see their own enrollments)
class StudentEnrollmentViewSet(viewsets.ModelViewSet):
    """Manages student-specific enrollments with filtering and caching."""
    serializer_class = EnrollmentSerializer
    pagination_class = EnrollmentPagination
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStudent]

    def get_cache_key(self) -> str:
        """
        Returns a unique cache key for the authenticated student's enrollments.
        """
        return f"enrollments_{self.request.user.pk}"

    def get_queryset(self):
        """
        Returns enrollments for the authenticated student.
        """
        user = self.request.user
        if user.is_authenticated:
            return Enrollment.objects.filter(student_email=user.email)
        return Enrollment.objects.none()

    @method_decorator(cache_page(30 * 60))
    @method_decorator(vary_on_cookie)
    def list(self, request: Request) -> Response:
        """
        Lists enrollments with caching enabled.
        """
        response = super().list(request)
        # Cache the response using the unique cache key
        cache.set(self.get_cache_key(), response.data, 30 * 60)
        return response

    def perform_create(self, serializer: BaseSerializer[Any]) -> None:
        """
        Handles enrollment creation and invalidates the cache.
        """
        serializer.save()
        self.invalidate_cache()

    def perform_update(self, serializer: BaseSerializer[Any]) -> None:
        """
        Handles enrollment update and invalidates the cache.
        """
        serializer.save()
        self.invalidate_cache()

    def perform_destroy(self, instance: Enrollment) -> None:
        """
        Handles enrollment deletion and invalidates the cache.
        """
        self.invalidate_cache()
        instance.delete()

    def invalidate_cache(self) -> None:
        """
        Deletes the cached enrollments for the authenticated student.
        """
        cache.delete(self.get_cache_key())