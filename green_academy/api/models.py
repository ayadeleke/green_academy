from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.core.exceptions import ValidationError

### Course model ###
class Course(models.Model):
    title = models.CharField(max_length=255, validators=[MinLengthValidator(5)])
    description = models.TextField()
    instructor = models.CharField(max_length=255)
    instructor_image = models.ImageField(upload_to='instructor_images/', blank=True, null=True)  # Optional
    start_date = models.DateField()
    end_date = models.DateField()

    def clean(self):
        """Ensures that the end date is later than the start date."""
        if self.start_date and self.end_date and self.start_date > self.end_date:
            raise ValidationError("End date must be later than start date")

    def save(self, *args, **kwargs):
        """Calls the clean method before saving."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        """Returns the title of the course as its string representation."""
        return self.title


### Enrollment model ###
class Enrollment(models.Model):
    student_id = models.CharField(max_length=50)
    student_name = models.CharField(max_length=255)
    student_email = models.EmailField()
    student_image = models.ImageField(upload_to='student_images/', blank=True, null=True)  # Optional
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student_id', 'course')  # Ensures a student can enroll only once per course

    def __str__(self) -> str:
        """Returns a formatted string representing the enrollment."""
        return f"{self.student_name} ({self.student_id}) - {self.course.title}"


# User Roles
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("instructor", "Instructor"),
        ("student", "Student"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="student")

    def __str__(self):
        return f"{self.user.username} - {self.role}"
