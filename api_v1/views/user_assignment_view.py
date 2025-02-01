from rest_framework import generics

from api_v1.permissions import CanCreateUserAssignment, CanDeleteUserAssignment, CanReadUserAssignment, CanUpdateUserAssignment
from core.models import UserAssignment
from api_v1.serializers import UserAssignmentSerializer, UserAssignmentSimpleSerializer


class UserAssignmentList(generics.ListCreateAPIView):
    serializer_class = UserAssignmentSerializer

    def get_queryset(self):
        """Filter by user ID if provided."""
        user_id = self.request.query_params.get("user")
        if user_id:
            return self.queryset.filter(user=user_id)
        return UserAssignment.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [CanReadUserAssignment]
        elif self.request.method == 'POST':
            self.permission_classes = [CanCreateUserAssignment]

        return super(UserAssignmentList, self).get_permissions()


class UserAssignmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserAssignment.objects.all()
    serializer_class = UserAssignmentSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [CanReadUserAssignment]
        elif self.request.method == 'DELETE':
            self.permission_classes = [CanDeleteUserAssignment]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [CanUpdateUserAssignment]

        return super(UserAssignmentDetail, self).get_permissions()
