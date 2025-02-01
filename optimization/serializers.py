from api_v1.serializers.base_serializer import BaseSerializer
from django_q.models import Task

class TaskSerializer(BaseSerializer):
    class Meta:
        model = Task
        fields = "__all__"