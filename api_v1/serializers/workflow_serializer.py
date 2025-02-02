from core.models import WorkflowTransition
from api_v1.serializers.base_serializer import BaseSerializer


class WorkflowTransitionSerializer(BaseSerializer):
    class Meta:
        model = WorkflowTransition
        fields = "__all__"