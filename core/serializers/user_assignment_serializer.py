from core.models import UserAssignment
from .base_serializer import BaseSerializer
from .category_serializer import CategorySerializer
from .user_serializer import UserSerializer



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

