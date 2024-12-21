from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from task_manager.models import CustomUser
from task_manager.serializers import UserSerializer
from task_manager.views.base_view import BaseAuthenticatedView


class UserList(BaseAuthenticatedView):
    def get(self, request: Request) -> Response:
        """
        Retrieve all users.
        """
        users = CustomUser.objects.prefetch_related('categories').all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(BaseAuthenticatedView):
    def get(self, request: Request, user_id: str) -> Response:
        """
        Retrieve a single user by ID.
        """
        try:
            user = request.user if user_id == "me" else CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User not found")

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# TODO: Implements user update only for yourself
