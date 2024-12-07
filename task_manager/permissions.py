from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has is_admin set to True
        return (request.user and request.user.is_authenticated 
                and getattr(request.user, 'is_admin', False))