
from rest_framework.response import Response
from rest_framework.request import Request

from core.models import Status
from core.serializers import StatusSerializer
from core.serializers.status_serializer import StatusSerializerWithTransition
from .base_view import BaseAuthenticatedView


class StatusList(BaseAuthenticatedView):
    input_serializer_class = StatusSerializer
    output_serializer_class = StatusSerializerWithTransition
    base_model_class = Status

    def get(self, request: Request) -> Response:
        """
        Retrieve all statuses.
        """
        return self.get_list()
    
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
        self.update_object(status_id, request.data)
