from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Allows access only to admin users."""
    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return request.user.is_authenticated and profile and getattr(profile, 'role', None) == "admin"

class IsInstructor(permissions.BasePermission):
    """Allows access only to instructors and admins."""
    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        role = getattr(profile, 'role', None)  # Get the role safely
        return request.user.is_authenticated and role in ["admin", "instructor"]


class IsStudent(permissions.BasePermission):
    """Allows access only to students."""
    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        return request.user.is_authenticated and profile and getattr(profile, 'role', None) == "student"

class IsAdminOrInstructorOrReadOnly(permissions.BasePermission):
    """Allows full access for admins and instructors, read-only for students."""
    def has_permission(self, request, view):
        profile = getattr(request.user, 'profile', None)
        role = getattr(profile, 'role', None)  # Get role safely

        if not request.user.is_authenticated or role is None:
            return False  # User must be authenticated and have a valid profile

        if role in ["admin", "instructor"]:
            return True  # Admins and instructors have full access

        if role == "student" and request.method in permissions.SAFE_METHODS:
            return True  # Students have read-only access (GET, HEAD, OPTIONS)

        return False  # Deny all other cases

