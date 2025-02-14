from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import CourseViewSet, EnrollmentViewSet, StudentEnrollmentViewSet

# Initialize the default router for automatic ViewSet handling
router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'my-enrollments', StudentEnrollmentViewSet, basename='my-enrollments')

# Define URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include router-generated routes
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # JWT token generation
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh JWT tokens
] + router.urls
