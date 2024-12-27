from core.models import Project
from core.serializers.base_serializer import BaseSerializer


class ProjectSerializer(BaseSerializer):
    class Meta:
        model = Project
        fields = "__all__"