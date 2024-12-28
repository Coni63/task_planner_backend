from rest_framework import serializers
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group
from core.models import Category, CustomUser
from .base_serializer import BaseSerializer
from .category_serializer import CategorySerializer


class UserSerializer(BaseSerializer):
    """
    Serializer for the User model to include relevant fields.
    """

    name = serializers.CharField(source='username')
    roles = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        slug_field='name',
        source='groups',
        queryset=Group.objects.all()
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
        # Get all categories (LEFT side of the "outer join")
        categories = Category.objects.all()
        
        # Get user assignments (RIGHT side of the "outer join")
        user_assignments = {assignment.category_id: assignment for assignment in user.userassignment_set.all()}
        
        ans = []
        
        for category in categories:
            # Check if this category has an assignment for the user
            assignment = user_assignments.get(category.id)
            
            # If an assignment exists, use its level; otherwise, default to "Blocked"
            ans.append({
                "id": assignment.id if assignment else None,
                "user": user.id,
                "category": CategorySerializer(category).data,
                "level": assignment.level if assignment else "Blocked"
            })
        
        return ans