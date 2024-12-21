from rest_framework import serializers

from task_manager.models import Status, Task, TaskAudit
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

    def validate(self, data):
        # check default constraints
        data = super().validate(data)

        # check custom constraints
        self.__check_task_not_closed(data)
        self.__check_active_state_without_picked_by(data)

        return data
    
    def __check_task_not_closed(self, data):
        # Even an admin cannot modified a closed task
        task = self.instance
        if task and task.status.state == "closed":
            raise serializers.ValidationError("Cannot update a closed task")

    def __check_active_state_without_picked_by(self, data):
        # Cannot set status to active or blocked without a user assigned
        status = data.get("status") or (self.instance.status if self.instance else None)
        picked_by = data.get("picked_by") or (self.instance.picked_by if self.instance else None)

        if status and status.state in ["active", "blocked", "closed"] and picked_by is None:
            raise serializers.ValidationError("Cannot set status to active, blocked, or closed without a user assigned")


class TaskAuditSerializer(BaseSerializer):
    class Meta:
        model = TaskAudit
        fields = "__all__"

class TaskOrderSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    order = serializers.IntegerField(allow_null=True)