from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Category,
    Status,
    CustomUser,
)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "first_name", "last_name", "is_member", "is_admin")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("first_name", "last_name", "username")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_member",
                    "is_admin",
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
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
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    list_display = ("title", "junior_factor", "senior_factor")
    search_fields = ("title",)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Statuses"

    list_display = ("status",)
    search_fields = ("status",)
