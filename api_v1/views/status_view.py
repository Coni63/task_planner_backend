from rest_framework import generics

from api_v1.permissions import CanCreateStatus, CanDeleteStatus, CanReadStatus, CanUpdateStatus
from core.models import Status
from api_v1.serializers import StatusSerializer


class StatusList(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [CanReadStatus]
        elif self.request.method == 'POST':
            self.permission_classes = [CanCreateStatus]

        return super(StatusList, self).get_permissions()


class StatusDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [CanReadStatus]
        elif self.request.method == 'DELETE':
            self.permission_classes = [CanDeleteStatus]
        elif self.request.method in ['PUT', 'PATCH']:
            self.permission_classes = [CanUpdateStatus]

        return super(StatusDetail, self).get_permissions()
