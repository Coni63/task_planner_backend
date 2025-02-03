import uuid
from django.urls import path, register_converter

from api_v1.views.workflow_view import WorkflowTransitionDetail, WorkflowTransitionList

from .views.menu_view import MenuView
from .views import (
    CategoryDetail,
    CategoryList,
    ProjectDetail,
    ProjectList,
    StatusDetail,
    StatusList,
    TaskDetail,
    TaskList,
    TaskListView,
    TaskPickView,
    UserAssignmentDetail,
    UserAssignmentList,
    UserDetail,
    UserList,
    OptimizerResult,
    Optimizer,
)
from core.auth import CustomTokenObtainPairView, CustomTokenRefreshView, LogoutView
from rest_framework_simplejwt.views import TokenVerifyView


class UUIDConverter:
    regex = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    def to_python(self, value):
        return uuid.UUID(value)

    def to_url(self, value):
        return str(value)


register_converter(UUIDConverter, "uuid")


urlpatterns = [
    path("menu/", MenuView.as_view(), name="menu-view"),
    path("users/", UserList.as_view(), name="user-list"),
    path("users/<uuid:pk>/", UserDetail.as_view(), name="user-detail"),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<uuid:pk>/", CategoryDetail.as_view(), name="category-detail"),
    path("user-assignement/", UserAssignmentList.as_view(), name="user-assignement-list"),
    path("user-assignement/<uuid:pk>/", UserAssignmentDetail.as_view(), name="user-assignement-detail"),
    path("projects/", ProjectList.as_view(), name="project-list"),
    path("projects/<uuid:pk>/", ProjectDetail.as_view(), name="project-detail"),
    path("status/", StatusList.as_view(), name="status-list"),
    path("status/<uuid:pk>/", StatusDetail.as_view(), name="status-detail"),
    path("workflow/", WorkflowTransitionList.as_view(), name="workflow-list"),
    path("workflow/<uuid:pk>/", WorkflowTransitionDetail.as_view(), name="workflow-detail"),
    path("tasks/", TaskList.as_view(), name="task-list"),
    path("tasks/<uuid:pk>/", TaskDetail.as_view(), name="task-detail"),
    path("task-pick/", TaskPickView.as_view(), name="task-pick"),
    path("tasks-history/", TaskListView.as_view(), name="task-history-list"),
    path("optimize/", Optimizer.as_view(), name="optimizer-submit"),
    path("optimize/<uuid:pk>/", OptimizerResult.as_view(), name="optimizer-status"),
    # Authentication
    path("auth/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("auth/token/logout/", LogoutView.as_view(), name="logout"),
]
