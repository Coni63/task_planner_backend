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
    TaskSimpleSerializer,
    UserAssignmentSerializer,
    UserAssignmentSimpleSerializer,
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
        user_id = request.query_params.get("user")
        if user_id:
            user_assignments = UserAssignment.objects.filter(user=user_id)
            if not user_assignments.exists():
                return Response([], status=status.HTTP_204_NO_CONTENT)
        else:
            user_assignments = UserAssignment.objects.all()

        serializer = UserAssignmentSerializer(user_assignments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = UserAssignmentSimpleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAssignmentDetail(APIView):
    """
    Handle user assignments for a specific user.
    """

    def get(self, request: Request, assignment_id: str) -> Response:
        try:
            user_assignments = UserAssignment.objects.get(pk=assignment_id)
        except UserAssignment.DoesNotExist:
            raise NotFound(detail="UserAssignment not found")

        serializer = UserAssignmentSerializer(user_assignments)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, assignment_id: str) -> Response:
        try:
            user_assignment = UserAssignment.objects.get(pk=assignment_id)
            user_assignment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserAssignment.DoesNotExist:
            raise NotFound(detail="UserAssignment not found")

    def put(self, request: Request, assignment_id: str) -> Response:
        try:
            user_assignment = UserAssignment.objects.get(pk=assignment_id)
        except UserAssignment.DoesNotExist:
            raise NotFound(detail="UserAssignment not found")

        serializer = UserAssignmentSerializer(user_assignment, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectList(APIView):
    def get(self, request: Request) -> Response:
        projects = Project.objects.all()  # noqa: F821
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = ProjectSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectDetail(APIView):
    def get(self, request: Request, project_id: str) -> Response:
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, project_id: str):
        try:
            project = Project.objects.get(pk=project_id)
            project.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

    def put(self, request: Request, project_id: str):
        try:
            project = Project.objects.get(pk=project_id)
        except Project.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = ProjectSerializer(project, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StatusList(APIView):
    def get(self, request: Request) -> Response:
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        return Response(serializer.data)


class StatusDetail(APIView):
    def get(self, request: Request, status_id: str) -> Response:
        try:
            records = Status.objects.get(pk=status_id)
        except Status.DoesNotExist:
            raise NotFound(detail="Status not found")

        serializer = StatusSerializer(records)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TaskList(APIView):
    def get(self, request: Request) -> Response:
        project_id = request.query_params.get("project")
        if project_id:
            tasks = Task.objects.filter(project=project_id)
            if not tasks.exists():
                return Response([], status=status.HTTP_204_NO_CONTENT)
        else:
            tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = TaskSimpleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetail(APIView):
    def get(self, request: Request, task_id: str) -> Response:
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound(detail="Task not found")

        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, task_id: str):
        try:
            task = Task.objects.get(pk=task_id)
            task.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Task.DoesNotExist:
            raise NotFound(detail="Project not found")

    def put(self, request: Request, task_id: str):
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            raise NotFound(detail="Project not found")

        serializer = TaskSimpleSerializer(task, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# TODO: Task Serializer with audit info

# TODO: All Users availability
# TODO: User availability get
# TODO: User availability create
# TODO: User availability update
# TODO: User availability delete

# TODO: Simplify with mixins ?
# TODO: Documentation and Authentication
