from rest_framework.response import Response
from rest_framework.request import Request

from task_manager.models import Project
from task_manager.serializers import ProjectSerializer
from task_manager.views.base_view import BaseAuthenticatedView


class ProjectList(BaseAuthenticatedView):
    base_serializer_class = Project
    base_model_class = ProjectSerializer

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
