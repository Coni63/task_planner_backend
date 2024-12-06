from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Task, CustomUser
from .serializers import TaskSerializer


from rest_framework import status
# from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from .serializers import UserSerializer


class UserList(APIView):
    """
    Retrieve all users or create a new user (if needed).
    """
    def get(self, request):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetail(APIView):
    """
    Retrieve a single user by ID.
    """
    def get_object(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound(detail="User not found")

    def get(self, request, user_id):
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# class TeamAssignmentList(APIView):
#     def get(self, request):
#         tasks = TeamAssignment.objects.all()  # noqa: F821
#         serializer = TeamAssignmentSerializer(tasks, many=True)
#         return Response(serializer.data)
    

# class TeamAssignmentList(APIView):
#     def get(self, request):
#         tasks = TeamAssignment.objects.all()  # noqa: F821
#         serializer = TeamAssignmentSerializer(tasks, many=True)
#         return Response(serializer.data)
    

class TaskList(APIView):
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
    

