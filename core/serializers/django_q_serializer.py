from core.serializers.base_serializer import BaseSerializer
from django_q.models import Task as DQTask

class DjangoQTaskSerializer(BaseSerializer):
    class Meta:
        model = DQTask
        fields = "__all__"