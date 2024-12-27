from django.urls import path

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



urlpatterns = [
    path("menu/", MenuView.as_view(), name="menu-view"),

    path("users/", UserList.as_view(), name="user-list"),
    path("users/<str:user_id>/", UserDetail.as_view(), name="user-detail"),

    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<str:category_id>/", CategoryDetail.as_view(), name="category-detail"),

    path("user-assignement/", UserAssignmentList.as_view(), name="user-assignement-list"),
    path("user-assignement/<str:assignment_id>/", UserAssignmentDetail.as_view(), name="user-assignement-detail"),
    
    path("projects/", ProjectList.as_view(), name="project-list"),
    path("projects/<str:project_id>/", ProjectDetail.as_view(), name="project-detail"),
    
    path("status/", StatusList.as_view(), name="status-list"),
    path("status/<str:status_id>/", StatusDetail.as_view(), name="status-detail"),
    
    path("tasks/", TaskList.as_view(), name="task-list"),
    path("tasks/<str:task_id>/", TaskDetail.as_view(), name="task-detail"),
    path("task-pick/", TaskPickView.as_view(), name="task-pick"),
    path("tasks-history/", TaskListView.as_view(), name="task-history-list"),

    path("optimize/", Optimizer.as_view(), name="optimizer-view"),
    path("optimize/<str:task_id>/", OptimizerResult.as_view(), name="optimizer-status"),

    # Authentication
    path('auth/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/token/logout/', LogoutView.as_view(), name='logout'),
]
