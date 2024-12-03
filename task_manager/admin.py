# from django.contrib import admin
# from .models import Team, TeamAssignment, Category, UserAssignment


# # Inline for TeamAssignment
# class TeamAssignmentInline(admin.TabularInline):
#     model = TeamAssignment
#     extra = 1  # Number of empty forms to show
#     autocomplete_fields = ('user',)  # Makes user selection easier

# # Register Category
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('title', 'junior_factor', 'senior_factor')
#     search_fields = ('title',)
#     list_filter = ('junior_factor', 'senior_factor')

# # Register Team
# @admin.register(Team)
# class TeamAdmin(admin.ModelAdmin):
#     list_display = ('name',)
#     search_fields = ('name',)
#     inlines = [TeamAssignmentInline]  # Use inline for managing members and roles


# # Register TeamAssignment
# @admin.register(TeamAssignment)
# class TeamAssignmentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'team', 'role')
#     search_fields = ('user__username', 'team__name')
#     list_filter = ('role',)
#     autocomplete_fields = ('user', 'team')  # For ForeignKey fields

# # Register UserAssignment
# @admin.register(UserAssignment)
# class UserAssignmentAdmin(admin.ModelAdmin):
#     list_display = ('user', 'category', 'assigned_date')
#     search_fields = ('user__username', 'category__title')
#     list_filter = ('assigned_date',)
#     autocomplete_fields = ('user', 'category')  # For ForeignKey fields
