from django.shortcuts import get_object_or_404
from rest_framework import generics

from api_v1.permissions import (
    CanCreateCustomUser,
    CanDeleteCustomUser,
    CanDeleteSomeoneElseCustomUser,
    CanReadCustomUser,
    CanUpdateCustomUser,
    CanUpdateSomeoneElseCustomUser,
    IsActiveUser,
)
from core.models import CustomUser
from api_v1.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.prefetch_related("categories").all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadCustomUser]
        elif self.request.method == "POST":
            self.permission_classes = [CanCreateCustomUser]

        return super(UserList, self).get_permissions()


class UserDetail(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    # TODO: Only allow to update some fields

    def get_permissions(self):
        is_me = self.request.user.id != self.kwargs.get("user_id")

        if self.request.method == "GET":
            self.permission_classes = [CanReadCustomUser]
        elif self.request.method == "DELETE":
            self.permission_classes = [CanDeleteCustomUser] if is_me else [CanDeleteSomeoneElseCustomUser]
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [CanUpdateCustomUser] if is_me else [CanUpdateSomeoneElseCustomUser]

        return super(UserDetail, self).get_permissions()

    def get_object(self):
        user_id = self.kwargs.get("pk")

        user = get_object_or_404(CustomUser, pk=user_id)
        self.check_object_permissions(self.request, user)
        return user


class MyselfDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_class = [IsActiveUser]

    # TODO: Lock the update of roles

    def get_object(self):
        return self.request.user
