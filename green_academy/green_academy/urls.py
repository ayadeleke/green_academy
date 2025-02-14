from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.urls import router

# Define the Swagger schema view for API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Green Academy API",
        default_version='v2',
        description="API documentation for Green Academy",
        terms_of_service="https://www.greenacademy.com/terms/",
        contact=openapi.Contact(email="support@greenacademy.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[AllowAny],  # Allows public access to API documentation
    authentication_classes=[],
)

# Define the URL patterns for routing requests
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin panel
    path('api/', include('api.urls')),  # Include API app URLs
    path('', include(router.urls)),  # Include router URLs for ViewSets
    path("api-auth/", include("rest_framework.urls")),  # DRF authentication endpoints

    # JWT Authentication Endpoints
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),  # Get access & refresh tokens
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),  # Refresh expired access tokens

    # API Documentation Endpoints
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),  # Swagger UI
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),  # ReDoc UI
]
