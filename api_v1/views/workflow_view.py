from rest_framework import generics

from core.models import WorkflowTransition
from api_v1.permissions import (
    CanReadWorkflowTransition,
    CanCreateWorkflowTransition,
    CanDeleteWorkflowTransition,
    CanUpdateWorkflowTransition,
)
from api_v1.serializers import WorkflowTransitionSerializer


class WorkflowTransitionList(generics.ListCreateAPIView):
    queryset = WorkflowTransition.objects.all()
    serializer_class = WorkflowTransitionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadWorkflowTransition]
        elif self.request.method == "POST":
            self.permission_classes = [CanCreateWorkflowTransition]

        return super(WorkflowTransitionList, self).get_permissions()


class WorkflowTransitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkflowTransition.objects.all()
    serializer_class = WorkflowTransitionSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadWorkflowTransition]
        elif self.request.method == "DELETE":
            self.permission_classes = [CanDeleteWorkflowTransition]
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [CanUpdateWorkflowTransition]

        return super(WorkflowTransitionDetail, self).get_permissions()
