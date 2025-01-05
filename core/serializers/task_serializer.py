from rest_framework import serializers

from core.models import Task
from .base_serializer import BaseSerializer
from .category_serializer import CategorySerializer
from .project_serializer import ProjectSerializer
from .status_serializer import StatusSerializer
from .user_serializer import UserSerializer


class TaskSerializer(BaseSerializer):
    status = StatusSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    picked_by = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    reserved_for_user = UserSerializer(read_only=True)
    at_risk = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = "__all__"

    def get_at_risk(self, task: Task):
        if task.estimated_finalization is None or task.expected_finalization is None:
            return False
        return task.estimated_finalization > task.expected_finalization


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
        self.__check_user_has_no_other_task(data)

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
        
    def __check_user_has_no_other_task(self, data):
        # Cannot set a user to a task if the user is already assigned to another task
        new_picked_by = data.get("picked_by")
        curr_picked_by = self.instance.picked_by if self.instance else None

        if new_picked_by is None:
            return
        
        if new_picked_by == curr_picked_by:
            return

        # check if the user is already assigned to another task
        tasks = Task.objects.filter(picked_by=new_picked_by).filter(status__state="active")
        if tasks.count() > 0:
            raise serializers.ValidationError("User is already assigned to another task")
