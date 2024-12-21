from task_manager.models import Category
from task_manager.serializers.base_serializer import BaseSerializer


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"