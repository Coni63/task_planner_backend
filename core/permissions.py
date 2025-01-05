from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has is_admin set to True
        return (request.user and request.user.is_authenticated 
                and "ADMIN" in [group.name for group in request.user.groups.all()])
    
class IsActiveUser(permissions.BasePermission):
    """
    Custom permission to only allow inactive users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and active
        return request.user and request.user.is_authenticated and request.user.is_active

class CustomJWTAuthentication(JWTAuthentication):
    pass
