from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

def _is_authenticated(request) -> bool:
    return request.user and request.user.is_authenticated and request.user.is_active

def _has_group(request, group: str) -> bool:
    return request.user.has_perm(f"core.{group}")


class CustomJWTAuthentication(JWTAuthentication):
    pass

class IsActiveUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request)

'''
Categories Permissions
'''
class CanReadCategories(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_category')


class CanUpdateCategories(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_category')


class CanDeleteCategories(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_category')


class CanCreateCategories(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_category')
    
'''
Project Permissions
'''
class CanReadProject(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_project')

class CanUpdateProject(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_project')

class CanDeleteProject(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_project')

class CanCreateProject(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_project')

'''
Status Permissions
'''
class CanReadStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_status')

class CanUpdateStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_status')

class CanDeleteStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_status')

class CanCreateStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_status')

'''
CustomUser Permissions
'''
class CanReadCustomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_customuser')

class CanUpdateCustomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_customuser')

class CanDeleteCustomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_customuser')

class CanCreateCustomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_customuser')

class CanUpdateSomeoneElseCustomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_someone_else_user')

class CanDeleteSomeoneElseCustomUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_someone_else_user')


'''
Task Permissions
'''
class CanReadTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_task')

class CanUpdateTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_task')

class CanDeleteTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_task')

class CanCreateTask(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_task')

'''
UserAssignment Permissions
'''
class CanReadUserAssignment(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_userassignment')

class CanUpdateUserAssignment(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_userassignment')

class CanDeleteUserAssignment(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_userassignment')

class CanCreateUserAssignment(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_userassignment')

'''
ScheduleRule Permissions
'''
class CanReadScheduleRule(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_schedulerule')

class CanUpdateScheduleRule(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_schedulerule')

class CanDeleteScheduleRule(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_schedulerule')

class CanCreateScheduleRule(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_schedulerule')

'''
ScheduleOverride Permissions
'''
class CanReadScheduleOverride(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_scheduleoverride')

class CanUpdateScheduleOverride(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_scheduleoverride')

class CanDeleteScheduleOverride(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_scheduleoverride')

class CanCreateScheduleOverride(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_scheduleoverride')

'''
Workflow Permissions
'''
class CanReadWorkflowTransition(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_workflowtransition')

class CanUpdateWorkflowTransition(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_workflowtransition')

class CanDeleteWorkflowTransition(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_workflowtransition')

class CanCreateWorkflowTransition(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_workflowtransition')
    

'''
DjangoQ Permissions
'''
class CanReadOrmQ(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'view_ormq')

class CanUpdateOrmQ(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'change_ormq')

class CanDeleteOrmQ(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'delete_ormq')

class CanCreateOrmQ(permissions.BasePermission):
    def has_permission(self, request, view):
        return _is_authenticated(request) and _has_group(request, 'add_ormq')