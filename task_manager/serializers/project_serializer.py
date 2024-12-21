from task_manager.models import Project
from task_manager.serializers.base_serializer import BaseSerializer


class ProjectSerializer(BaseSerializer):
    class Meta:
        model = Project
        fields = "__all__"