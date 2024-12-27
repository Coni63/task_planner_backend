from rest_framework.response import Response
from rest_framework.request import Request
from django_q.tasks import async_task, fetch

from core.serializers.django_q_serializer import DjangoQTaskSerializer

from .base_view import BaseAuthenticatedView


class Optimizer(BaseAuthenticatedView):
    def post(self, request: Request) -> Response:
        task_id = async_task('optimization.services.optimize', request.data)
        return Response({"task_id": task_id})


class OptimizerResult(BaseAuthenticatedView):
    def get(self, request: Request, task_id: str) -> Response:
        task = fetch(task_id)
        return Response(DjangoQTaskSerializer(task).data)