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
    roles = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='groups'
    )
    permissions = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()  # Custom field for categories with levels


    class Meta:
        model = CustomUser
        fields = ("id", "name", "email", "first_name", "last_name", "is_member", "is_admin", "roles", "permissions", "avatar", "categories")
    
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
        return user.avatar if user.avatar else "https://ng-matero.github.io/ng-matero/images/avatar.jpg"


    def get_categories(self, user: CustomUser):
        """
        Return all categories with their corresponding skill level for the user.
        """
        # Get all categories
        categories = Category.objects.all()
        
        # Get user assignments for the given user
        user_assignments = UserAssignment.objects.filter(user=user)
        
        # Serialize each category and attach the user's level (or "Blocked" if no assignment exists)
        ans = [
            {
                "id": None,
                "user": user.id,
                "category": CategorySerializer(category).data,
                "level": "Blocked"
            }
            for category in categories
        ]
        for assignment in user_assignments:
            for i, category in enumerate(ans):
                if category["category"]["id"] == str(assignment.category.id):
                    ans[i]["id"] = assignment.id
                    ans[i]["level"] = assignment.level
                    break

        return ans


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
    picked_by = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    estimated_finalization = serializers.SerializerMethodField()
    at_risk = serializers.SerializerMethodField()
    
    class Meta:
        model = Task
        fields = "__all__"

    def get_estimated_finalization(self, task):
        return task.expected_finalization  # TODO: real computation
    
    def get_at_risk(self, task):
        estimated_finalization = self.get_estimated_finalization(task)
        if estimated_finalization is None or estimated_finalization is None:
            return False
        return self.get_estimated_finalization(task) > task.expected_finalization


class TaskSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskAuditSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAudit
        fields = "__all__"


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


class TaskOrderSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    order = serializers.IntegerField(allow_null=True)