from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound

from .models import Category, Project, Status, Task, CustomUser, UserAssignment
from .serializers import (
    CategorySerializer,
    ProjectSerializer,
    StatusSerializer,
    TaskSerializer,
    UserAssignmentSerializer,
    UserSerializer,
)


class UserList(APIView):
    """
    Retrieve all users.
    """

    def get(self, request: Request) -> Response:
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(APIView):
    """
    Retrieve a single user by ID.
    """

    def get(self, request: Request, user_id: str) -> Response:
        try:
            user = CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User not found")

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryList(APIView):
    """
    Retrieve all categories.
    """

    def get(self, request: Request) -> Response:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserAssignmentList(APIView):
    """
    Retrieve all user assignments.
    """

    def get(self, request: Request) -> Response:
        tasks = UserAssignment.objects.all()  # noqa: F821
        serializer = UserAssignmentSerializer(tasks, many=True)
        return Response(serializer.data)


class UserAssignmentDetail(APIView):
    """
    Retrieve all user assignments of a single user by user ID.
    """

    def get(self, request: Request, user_id: str) -> Response:
        user_assignments = UserAssignment.objects.filter(user=user_id)

        if not user_assignments.exists():
            raise NotFound(detail="No assignments found for the specified user")

        serializer = UserAssignmentSerializer(user_assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO: UserAssignmentCreate


class ProjectList(APIView):
    def get(self, request: Request) -> Response:
        projects = Project.objects.all()  # noqa: F821
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)


class ProjectDetail(APIView):
    def get(self, request: Request, project_id: str) -> Response:
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StatusList(APIView):
    def get(self, request: Request) -> Response:
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)


class StatusDetail(APIView):
    def get(self, request: Request, status_id: str) -> Response:
        try:
            status = Status.objects.get(pk=status_id)
        except Status.DoesNotExist:
            raise NotFound(detail="Status not found")

        serializer = StatusSerializer(status)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskList(APIView):
    def get(self, request: Request) -> Response:
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskDetail(APIView):
    def get(self, request: Request, task_id: str) -> Response:
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found")

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)


# TODO: TaskCreate
# TODO: TaskUpdate
# TODO: TaskDelete
# TODO: Serializer with audit info
