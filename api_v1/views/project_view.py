from rest_framework.response import Response
from rest_framework.request import Request

from core.models import Project
from core.serializers import ProjectSerializer
from .base_view import BaseAuthenticatedView


class ProjectList(BaseAuthenticatedView):
    input_serializer_class = ProjectSerializer
    output_serializer_class = ProjectSerializer
    base_model_class = Project

    def get(self, request: Request) -> Response:
        """	
        Retrieve all projects.
        """
        return self.get_list()

    def post(self, request: Request) -> Response:
        """
        Create a new project.
        """
        return self.create_object(request.data)


class ProjectDetail(BaseAuthenticatedView):
    input_serializer_class = ProjectSerializer
    output_serializer_class = ProjectSerializer
    base_model_class = Project

    def get(self, request: Request, project_id: str) -> Response:
        """
        Retrieve a single project by ID.
        """
        return self.get_object(project_id)

    def delete(self, request: Request, project_id: str):
        """
        Delete a project by ID.
        """
        return self.delete_object(project_id)

    def put(self, request: Request, project_id: str):
        """
        Update a project by ID.
        """
        return self.update_object(project_id, request.data)
