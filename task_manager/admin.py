from django.contrib import admin
from .models import (
    Team,
    Category,
    TeamAssignment,
    UserAssignment,
    Project,
    Status,
    Task,
    TaskAudit
)

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'junior_factor', 'senior_factor')
    search_fields = ('title',)


@admin.register(TeamAssignment)
class TeamAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'team_id', 'is_admin', 'is_member')
    list_filter = ('is_admin', 'is_member')
    search_fields = ('user_id__username', 'team_id__name')


@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'category_id', 'level')
    list_filter = ('level',)
    search_fields = ('user_id__username', 'category_id__title')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team_id', 'description')
    search_fields = ('name', 'team_id__name')
    list_filter = ('team_id',)


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
    search_fields = ('title', 'project_id__name', 'assigned_user_id__username')
    autocomplete_fields = ('status_id', 'project_id', 'assigned_user_id', 'category_id')
    filter_horizontal = ('dependencies',)


@admin.register(TaskAudit)
class TaskAuditAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'status_id', 'user_id', 'updated_at')
    list_filter = ('status_id', 'user_id')
    search_fields = ('task_id__title', 'status_id__status', 'user_id__username')
