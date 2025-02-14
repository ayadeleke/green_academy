from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == "admin"

class IsInstructor(permissions.BasePermission):
    """Allows access only to instructors and admins."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role in ["admin", "instructor"]

class IsStudent(permissions.BasePermission):
    """Allows access only to students."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, 'profile') and request.user.profile.role == "student"

class IsAdminOrInstructorOrReadOnly(permissions.BasePermission):
    """Allows full access for admins and instructors, read-only for students."""
    def has_permission(self, request, view):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            # Full access for Admins & Instructors
            if request.user.profile.role in ["admin", "instructor"]:
                return True
            # Read-only access for students
            if request.user.profile.role == "student" and request.method in ["GET", "HEAD", "OPTIONS"]:
                return True
        return False
