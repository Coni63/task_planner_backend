from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from core.models import CustomUser
from core.serializers import UserSerializer
from .base_view import BaseAuthenticatedView


class UserList(BaseAuthenticatedView):
    def get(self, request: Request) -> Response:
        """
        Retrieve all users.
        """
        users = CustomUser.objects.prefetch_related('categories').all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(BaseAuthenticatedView):
    input_serializer_class = UserSerializer
    output_serializer_class = UserSerializer
    base_model_class = CustomUser

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

    def patch(self, request: Request, user_id: str) -> Response:
        """
        Update a single user by ID.
        """
        me: CustomUser = request.user
        data = request.data
        target_user_id = me.id if user_id == "me" else user_id
        update_self = target_user_id == str(me.id)

        # Check if the logged-in user is admin
        is_admin = "ADMIN" in [group.name for group in me.groups.all()]

        # Restrict keys an admin can update
        admin_allowed_keys = {"id", "roles"}  # id is mandatory but will not be updated
        updated_keys = set(data.keys())
        update_roles = updated_keys.issubset(admin_allowed_keys)

        # Restrict updates to self unless admin
        if not update_self and not is_admin:
            return Response("You can only update your own data unless you are an admin.", status=status.HTTP_403_FORBIDDEN)

        if update_self and update_roles:
            return Response("You cannot update your roles directly.", status=status.HTTP_403_FORBIDDEN)

        return self.patch_object(target_user_id, data)
    
    def put(self, request: Request, user_id: str) -> Response:
        """
        Update a single user by ID.
        """
        me: CustomUser = request.user
        target_user_id = me.id if user_id == "me" else user_id

        if target_user_id != str(me.id):
            return Response("You cannot edit someone else information", status=status.HTTP_403_FORBIDDEN)
        
        return self.update_object(self, target_user_id, request.data)

