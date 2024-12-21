from rest_framework import serializers
from task_manager.serializers.base_serializer import BaseSerializer


class SearchModelSerializer(BaseSerializer):
    value = serializers.CharField(max_length=255, required=False, allow_blank=True)
    regex = serializers.BooleanField()
    fixed = serializers.ListField(child=serializers.CharField(), required=False)


class ColumnModelSerializer(BaseSerializer):
    data = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    searchable = serializers.BooleanField()
    orderable = serializers.BooleanField()
    search = SearchModelSerializer()


class OrderModelSerializer(BaseSerializer):
    column = serializers.IntegerField()
    dir = serializers.ChoiceField(choices=["asc", "desc"])
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)


class SearchRequestModelSerializer(BaseSerializer):
    draw = serializers.IntegerField(default=0)
    columns = ColumnModelSerializer(many=True)
    order = OrderModelSerializer(many=True)
    start = serializers.IntegerField(default=0)
    length = serializers.IntegerField(required=False, allow_null=True)
    search = SearchModelSerializer(required=False, allow_null=True)

