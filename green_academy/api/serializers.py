from typing import Any, Dict
from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from rest_framework import serializers
from api.models import Course, Enrollment


# Course Serializer (Ensures title uniqueness & valid dates)
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'instructor', 'instructor_image', 'start_date', 'end_date']
        extra_kwargs = {'instructor_image': {'required': False}}

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Custom validation for course creation and updates."""
        start_date = data.get("start_date")
        instructor = data.get("instructor")
        end_date = data.get("end_date")
        title = data.get("title")

        # Ensure the end date is later than the start date
        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError("End date must be later than start date")

        # Prevent duplicate courses by the same instructor with the same title
        if instructor and title and Course.objects.filter(instructor=instructor, title=title).exists():
            raise serializers.ValidationError("This instructor already has a course with this title")

        # Prevent duplicate course titles
        if title and Course.objects.filter(title=title).exists():
            raise serializers.ValidationError("A course with this title already exists")

        return data


# Enrollment Serializer (Ensures student email & prevents duplicate enrollments)
class EnrollmentSerializer(serializers.ModelSerializer):
    student_email = serializers.EmailField(
        validators=[EmailValidator()]  # Ensures a valid email
    )

    student_id = serializers.CharField(max_length=50)

    course = serializers.SlugRelatedField(
        queryset=Course.objects.all(),
        slug_field='title'
    )

    start_date = serializers.DateField(source='course.start_date', read_only=True)
    end_date = serializers.DateField(source='course.end_date', read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'student_id', 'student_name', 'student_email', 'student_image', 'start_date', 'end_date',
                  'course', 'enrollment_date']
        extra_kwargs = {'student_image': {'required': False}}

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Custom validation to prevent duplicate enrollments."""
        student_id = data.get("student_id")
        student_email = data.get("student_email")
        course = data.get("course")

        # Ensure student_id is valid
        if not isinstance(student_id, str):
            raise serializers.ValidationError({"student_id": "Invalid student ID format."})

        # Validate course existence
        if not Course.objects.filter(title=course.title).exists():
            raise serializers.ValidationError({"course": "Invalid course selection."})

        # Avoid duplicate enrollment
        if Enrollment.objects.filter(student_id=student_id, course=course, student_email=student_email).exists():
            raise serializers.ValidationError("This student is already enrolled in this course.")
        return data
