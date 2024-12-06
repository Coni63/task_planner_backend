from rest_framework import serializers
from .models import CustomUser, Task
# from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model to include relevant fields.
    """
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name')  # Include fields as needed


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


# class TeamAssignmentSerializer(serializers.ModelSerializer):
#     user_info = UserSerializer(source='user_id', read_only=True)
    
#     class Meta:
#         model = TeamAssignment
#         fields = '__all__'