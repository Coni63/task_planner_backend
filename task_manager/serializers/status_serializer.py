
from task_manager.models import Status
from task_manager.serializers.base_serializer import BaseSerializer


class StatusSerializer(BaseSerializer):
    class Meta:
        model = Status
        fields = "__all__"