from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Category,
    UserAssignment,
    Project,
    Status,
    Task,
    TaskAudit,
    ScheduleRule,
    ScheduleOverride,
    CustomUser,
)


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
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2", "is_staff", "is_active"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "junior_factor", "senior_factor")
    search_fields = ("title",)


@admin.register(UserAssignment)
class UserAssignmentAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "level")
    list_filter = ("level",)
    search_fields = ("user__username", "category__title")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)
    # list_filter = ()


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("status",)
    search_fields = ("status",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "project", "assigned_user", "picked_at", "expected_finalization")
    list_filter = ("status", "project", "assigned_user")
    search_fields = ("title", "project__name", "assigned_user__username")
    autocomplete_fields = ("status", "project", "assigned_user", "category")
    filter_horizontal = ("dependencies",)


@admin.register(TaskAudit)
class TaskAuditAdmin(admin.ModelAdmin):
    list_display = ("task", "status", "user", "updated_at")
    list_filter = ("status", "user")
    search_fields = ("task__title", "status__status", "user__username")


@admin.register(ScheduleRule)
class ScheduleRuleAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScheduleRule.
    """

    list_display = ("user", "day_of_week", "factor", "start_date", "end_date")
    list_filter = ("day_of_week", "factor", "start_date", "end_date")
    search_fields = ("user__username", "user__email")
    ordering = ("user", "day_of_week", "start_date", "end_date")
    fieldsets = (
        (None, {"fields": ("user", "day_of_week", "factor")}),
        (
            "Optional Date Range",
            {
                "fields": ("start_date", "end_date"),
                "classes": ("collapse",),  # Makes the section collapsible in the admin
            },
        ),
    )


@admin.register(ScheduleOverride)
class ScheduleOverrideAdmin(admin.ModelAdmin):
    """
    Admin configuration for ScheduleOverride.
    """

    list_display = ("user", "date", "factor")
    list_filter = ("date", "factor")
    search_fields = ("user__username", "user__email", "date")
    ordering = ("user", "date")
