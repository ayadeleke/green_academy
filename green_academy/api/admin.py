from django.contrib import admin
from api.models import Course, Enrollment, UserProfile  # Import UserProfile

# Register your models here
admin.site.register(Course)
admin.site.register(Enrollment)
admin.site.register(UserProfile) 
