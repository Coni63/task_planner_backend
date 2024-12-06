from django.contrib import admin
from .models import (
    Category,
    UserAssignment,
    Project,
    Status,
    Task,
    TaskAudit,
    ScheduleRule, ScheduleOverride
)
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "is_staff")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_active"),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'junior_factor', 'senior_factor')
    search_fields = ('title',)

@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'category_id', 'level')
    list_filter = ('level',)
    search_fields = ('user_id__user_name', 'category_id__title')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
    # list_filter = ()


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('status',)
    search_fields = ('status',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'title', 
        'status_id', 
        'project_id', 
        'assigned_user_id', 
        'picked_at', 
        'expected_finalization'
    )
    list_filter = ('status_id', 'project_id', 'assigned_user_id')
    search_fields = ('title', 'project_id__name', 'assigned_user_id__user_name')
    autocomplete_fields = ('status_id', 'project_id', 'assigned_user_id', 'category_id')
    filter_horizontal = ('dependencies',)


@admin.register(TaskAudit)
class TaskAuditAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'status_id', 'user_id', 'updated_at')
    list_filter = ('status_id', 'user_id')
    search_fields = ('task_id__title', 'status_id__status', 'user_id__user_name')



@admin.register(ScheduleRule)
class ScheduleRuleAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScheduleRule.
    """
    list_display = ('user_id', 'day_of_week', 'factor', 'start_date', 'end_date')
    list_filter = ('day_of_week', 'factor', 'start_date', 'end_date')
    search_fields = ('user_id__user_name', 'user_id__email')
    ordering = ('user_id', 'day_of_week', 'start_date', 'end_date')
    fieldsets = (
        (None, {
            'fields': ('user_id', 'day_of_week', 'factor')
        }),
        ('Optional Date Range', {
            'fields': ('start_date', 'end_date'),
            'classes': ('collapse',),  # Makes the section collapsible in the admin
        }),
    )

@admin.register(ScheduleOverride)
class ScheduleOverrideAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScheduleOverride.
    """
    list_display = ('user_id', 'date', 'factor')
    list_filter = ('date', 'factor')
    search_fields = ('user_id__user_name', 'user_id__email', 'date')
    ordering = ('user_id', 'date')