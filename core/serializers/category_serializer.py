from core.models import Category
from core.serializers.base_serializer import BaseSerializer


class CategorySerializer(BaseSerializer):
    class Meta:
        model = Category
        fields = "__all__"