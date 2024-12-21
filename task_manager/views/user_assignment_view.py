from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request

from task_manager.models import UserAssignment
from task_manager.serializers import UserAssignmentSerializer, UserAssignmentSimpleSerializer
from task_manager.views.base_view import BaseAuthenticatedView


class UserAssignmentList(BaseAuthenticatedView):
    input_serializer_class = UserAssignmentSimpleSerializer
    output_serializer_class = UserAssignmentSerializer
    base_model_class = UserAssignment

    def get(self, request: Request) -> Response:
        """
        Retrieve all user assignments or for a single user (by id with query param 'user')
        """
        user_id = request.query_params.get("user")
        if user_id:
            user_assignments = UserAssignment.objects.filter(user=user_id)
        else:
            user_assignments = UserAssignment.objects.all()

        if not user_assignments.exists():
            return Response([], status=status.HTTP_200_OK)

        serializer = UserAssignmentSerializer(user_assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        """
        Create a new user assignment.
        """
        return self.create_object(request.data)


class UserAssignmentDetail(BaseAuthenticatedView):
    input_serializer_class = UserAssignmentSimpleSerializer
    output_serializer_class = UserAssignmentSerializer
    base_model_class = UserAssignment

    def get(self, request: Request, assignment_id: str) -> Response:
        """
        Get a single user assignment by id.
        """
        return self.get_object(assignment_id)

    def delete(self, request: Request, assignment_id: str) -> Response:
        """
        Delete a user assignment by id.
        """
        return self.delete_object(assignment_id)

    def put(self, request: Request, assignment_id: str) -> Response:
        """
        Update a user assignment by id.
        """
        return self.update_object(assignment_id, request.data)
