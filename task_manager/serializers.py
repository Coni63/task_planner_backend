from rest_framework import serializers
from .models import (
    Category,
    CustomUser,
    Project,
    Status,
    Task,
    TaskAudit,
    UserAssignment,
)
from django.contrib.auth.models import Permission


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model to include relevant fields.
    """

    name = serializers.CharField(source='username')
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    isMember = serializers.BooleanField(source='is_member')
    isAdmin = serializers.BooleanField(source='is_admin')
    roles = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='groups'
    )
    permissions = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "firstName", "lastName", "isMember", "isAdmin", "roles", "permissions", "avatar")
    
    def get_permissions(self, user):
        """
        Return a list of unique permissions for the user, including permissions granted via groups.
        """
        # Get user-specific permissions
        user_permissions = user.user_permissions.values_list('codename', flat=True)
        
        # Get permissions from groups the user belongs to
        group_permissions = Permission.objects.filter(group__user=user).values_list('codename', flat=True)
        
        # Combine user-specific permissions with group-based permissions and remove duplicates
        all_permissions = set(user_permissions).union(set(group_permissions))
        
        return list(all_permissions)
    
    def get_avatar(self, user):
        # TODO: add avatar in model
        return "https://ng-matero.github.io/ng-matero/images/avatar.jpg"
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class UserAssignmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = UserAssignment
        fields = "__all__"


class UserAssignmentSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAssignment
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class TaskSerializer(serializers.ModelSerializer):
    status = StatusSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)
    assigned_user = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = Task
        fields = "__all__"


class TaskSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAudit
        fields = "__all__"
