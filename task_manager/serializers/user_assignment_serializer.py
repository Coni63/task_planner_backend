from task_manager.models import UserAssignment
from task_manager.serializers.base_serializer import BaseSerializer
from task_manager.serializers.category_serializer import CategorySerializer
from task_manager.serializers.user_serializer import UserSerializer



class UserAssignmentSerializer(BaseSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = UserAssignment
        fields = "__all__"


class UserAssignmentSimpleSerializer(BaseSerializer):
    class Meta:
        model = UserAssignment
        fields = "__all__"

