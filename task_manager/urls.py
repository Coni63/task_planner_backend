from django.urls import path
from .views import (
    CategoryList,
    ProjectDetail,
    ProjectList,
    StatusDetail,
    StatusList,
    UserAssignmentDetail,
    UserAssignmentList,
    UserDetail,
    UserList,
)


urlpatterns = [
    # path('tasks/', TaskList.as_view(), name='task-list'),
    path("users/", UserList.as_view(), name="user-list"),
    path("users/<str:user_id>/", UserDetail.as_view(), name="user-detail"),
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("user-assignement/", UserAssignmentList.as_view(), name="user-assignement-list"),
    path("user-assignement/<str:user_id>/", UserAssignmentDetail.as_view(), name="user-assignement-details"),
    path("projects/", ProjectList.as_view(), name="project-list"),
    path("projects/<str:project_id>/", ProjectDetail.as_view(), name="project-list"),
    path("status/", StatusList.as_view(), name="status-list"),
    path("status/<str:status_id>/", StatusDetail.as_view(), name="status-list"),
]
