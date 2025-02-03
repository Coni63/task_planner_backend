from rest_framework import generics

from api_v1.permissions import IsActiveUser, IsOwnerOrReadOnly
from core.models import CustomUser
from api_v1.serializers import UserSerializer


class UserList(generics.ListAPIView):
    queryset = CustomUser.objects.prefetch_related("categories").all()
    serializer_class = UserSerializer
    permission_classes = [IsActiveUser, IsOwnerOrReadOnly]


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.prefetch_related("categories").all()
    serializer_class = UserSerializer
    permission_classes = [IsActiveUser, IsOwnerOrReadOnly]

    # TODO: lock change of roles
