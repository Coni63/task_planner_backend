from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import views
from rest_framework.exceptions import ValidationError
from django_q.tasks import async_task, fetch

from api_v1.permissions import CanCreateOrmQ, CanReadOrmQ
from api_v1.serializers.django_q_serializer import DjangoQTaskSerializer
from core.models.project import Project


class Optimizer(views.APIView):
    permission_classes = [CanCreateOrmQ]

    def post(self, request: Request) -> Response:
        project_id = request.data.get("project_id")  # the middleware change the camelcase to snakecase
        if not project_id:
            raise ValidationError("Missing 'projectId'")

        if not Project.objects.get(pk=project_id):
            raise ValidationError(f"Project '{project_id}' not found")

        task_id = async_task("optimization.services.optimize", request.data)
        return Response({"task_id": task_id})


class OptimizerResult(views.APIView):
    permission_classes = [CanReadOrmQ]

    def get(self, request: Request, pk: str) -> Response:
        task = fetch(pk)
        return Response(DjangoQTaskSerializer(task).data)
