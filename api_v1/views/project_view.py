from rest_framework import generics
from api_v1.permissions import CanCreateProject, CanDeleteProject, CanReadProject, CanUpdateProject
from core.models import Project
from api_v1.serializers import ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadProject]
        elif self.request.method == "POST":
            self.permission_classes = [CanCreateProject]

        return super(ProjectList, self).get_permissions()


class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.request.method == "GET":
            self.permission_classes = [CanReadProject]
        elif self.request.method == "DELETE":
            self.permission_classes = [CanDeleteProject]
        elif self.request.method in ["PUT", "PATCH"]:
            self.permission_classes = [CanUpdateProject]

        return super(ProjectDetail, self).get_permissions()
