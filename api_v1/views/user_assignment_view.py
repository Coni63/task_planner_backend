from rest_framework import generics

from api_v1.permissions import (
    CanCreateUserAssignment,
    CanDeleteUserAssignment,
    CanReadUserAssignment,
    CanUpdateUserAssignment,
)
from core.models import UserAssignment
from api_v1.serializers import UserAssignmentSerializer
from django_filters import rest_framework as filters


class UserAssignmentFilter(filters.FilterSet):
    class Meta:
        model = UserAssignment
        fields = ["user"]


class UserAssignmentList(generics.ListCreateAPIView):
    queryset = UserAssignment.objects.all()
    serializer_class = UserAssignmentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = UserAssignmentFilter

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadUserAssignment]
        elif self.request.method == "POST":
            self.permission_classes = [CanCreateUserAssignment]

        return super(UserAssignmentList, self).get_permissions()


class UserAssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAssignment.objects.all()
    serializer_class = UserAssignmentSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadUserAssignment]
        elif self.request.method == "DELETE":
            self.permission_classes = [CanDeleteUserAssignment]
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [CanUpdateUserAssignment]

        return super(UserAssignmentDetail, self).get_permissions()
