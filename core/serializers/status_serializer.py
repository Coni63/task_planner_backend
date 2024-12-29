
from core.models import Status, WorkflowTransition
from core.serializers.base_serializer import BaseSerializer
from rest_framework import serializers

class StatusSerializer(BaseSerializer):
    class Meta:
        model = Status
        fields = "__all__"

    
class StatusSerializerWithTransition(BaseSerializer):
    transitions = serializers.SerializerMethodField()

    class Meta:
        model = Status
        fields = "__all__"

    def get_transitions(self, obj):
        """
        Returns a list of the next statuses related to the current status
        based on workflow transitions.
        """
        transitions = WorkflowTransition.objects.filter(from_status=obj)
        return [
            StatusSerializer(transition.to_status).data for transition in transitions
        ]