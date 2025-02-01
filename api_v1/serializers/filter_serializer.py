from rest_framework import serializers



class SearchModelSerializer(serializers.Serializer):
    value = serializers.CharField(max_length=255, required=False, allow_blank=True)
    regex = serializers.BooleanField()
    fixed = serializers.ListField(child=serializers.CharField(), required=False)


class ColumnModelSerializer(serializers.Serializer):
    data = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)
    searchable = serializers.BooleanField()
    orderable = serializers.BooleanField()
    search = SearchModelSerializer()


class OrderModelSerializer(serializers.Serializer):
    column = serializers.IntegerField()
    dir = serializers.ChoiceField(choices=["asc", "desc"])
    name = serializers.CharField(max_length=255, required=False, allow_blank=True)


class SearchRequestModelSerializer(serializers.Serializer):
    draw = serializers.IntegerField(default=0)
    columns = ColumnModelSerializer(many=True)
    order = OrderModelSerializer(many=True)
    start = serializers.IntegerField(default=0)
    length = serializers.IntegerField(required=False, allow_null=True)
    search = SearchModelSerializer(required=False, allow_null=True)

