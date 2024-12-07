from rest_framework import serializers
from .models import (
    Category,
    CustomUser,
    Project,
    Status,
    Task,
    TaskAudit,
    UserAssignment,
)


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model to include relevant fields.
    """

    class Meta:
        model = CustomUser
        fields = ("id", "username", "email", "first_name", "last_name", "is_member", "is_admin")


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UserAssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = UserAssignment
        fields = "__all__"


class UserAssignmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssignment
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    assigned_user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = "__all__"


class TaskSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAudit
        fields = "__all__"
