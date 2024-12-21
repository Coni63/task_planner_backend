from rest_framework import serializers

from task_manager.models import Task, TaskAudit
from task_manager.serializers.base_serializer import BaseSerializer
from task_manager.serializers.category_serializer import CategorySerializer
from task_manager.serializers.project_serializer import ProjectSerializer
from task_manager.serializers.status_serializer import StatusSerializer
from task_manager.serializers.user_serializer import UserSerializer


class TaskSerializer(BaseSerializer):
    status = StatusSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    picked_by = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    estimated_finalization = serializers.SerializerMethodField()
    at_risk = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = "__all__"

    def get_estimated_finalization(self, task):
        return task.expected_finalization  # TODO: real computation
    
    def get_at_risk(self, task):
        estimated_finalization = self.get_estimated_finalization(task)
        if estimated_finalization is None or estimated_finalization is None:
            return False
        return self.get_estimated_finalization(task) > task.expected_finalization


class TaskSimpleSerializer(BaseSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskAuditSerializer(BaseSerializer):
    class Meta:
        model = TaskAudit
        fields = "__all__"

class TaskOrderSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    order = serializers.IntegerField(allow_null=True)