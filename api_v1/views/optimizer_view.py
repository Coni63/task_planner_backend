from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import views
from django_q.tasks import async_task, fetch

from api_v1.permissions import CanCreateOrmQ, CanReadOrmQ
from api_v1.serializers.django_q_serializer import DjangoQTaskSerializer


class Optimizer(views.APIView):
    permission_classes = [CanCreateOrmQ]

    def post(self, request: Request) -> Response:
        task_id = async_task('optimization.services.optimize', request.data)
        return Response({"task_id": task_id})


class OptimizerResult(views.APIView):
    permission_classes = [CanReadOrmQ]

    def get(self, request: Request, pk: str) -> Response:
        task = fetch(pk)
        if not task:
            return Response({})
        return Response(DjangoQTaskSerializer(task).data)