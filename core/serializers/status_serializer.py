
from core.models import Status
from core.serializers.base_serializer import BaseSerializer


class StatusSerializer(BaseSerializer):
    class Meta:
        model = Status
        fields = "__all__"