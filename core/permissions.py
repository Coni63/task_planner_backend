from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow admin users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and has is_admin set to True
        return (request.user and request.user.is_authenticated 
                and getattr(request.user, 'is_admin', False))
    
class IsActiveUser(permissions.BasePermission):
    """
    Custom permission to only allow inactive users.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and active
        return request.user and request.user.is_authenticated and request.user.is_active

class CustomJWTAuthentication(JWTAuthentication):
    pass
