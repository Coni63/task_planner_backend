
from rest_framework.response import Response
from rest_framework.request import Request

from core.models import Status
from core.serializers import StatusSerializer
from core.serializers.status_serializer import StatusSerializerWithTransition
from .base_view import BaseAuthenticatedView
from rest_framework import status

class StatusList(BaseAuthenticatedView):
    input_serializer_class = StatusSerializer
    output_serializer_class = StatusSerializerWithTransition
    base_model_class = Status

    def get(self, request: Request) -> Response:
        """
        Retrieve all statuses.
        """
        statuses = Status.objects.prefetch_related('transitions_from__to_status').all()
        serializer = StatusSerializerWithTransition(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request: Request) -> Response:
        """
        Create a new status.
        """
        return self.create_object(request.data)


class StatusDetail(BaseAuthenticatedView):
    input_serializer_class = StatusSerializer
    output_serializer_class = StatusSerializerWithTransition
    base_model_class = Status
    
    def get(self, request: Request, status_id: str) -> Response:
        """
        Retrieve a single status by ID.
        """
        return self.get_object(status_id)

    def delete(self, request: Request, status_id: str) -> Response:
        """
        Delete a status by ID.
        """
        return self.delete_object(status_id)

    def put(self, request: Request, status_id: str) -> Response:
        """
        Update a status by ID.
        """
        return self.update_object(status_id, request.data)
