from django.urls import include, path
from .views import TaskList, UserDetail, UserList

urlpatterns = [
    # path('tasks/', TaskList.as_view(), name='task-list'),
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetail.as_view(), name='user-detail'),
    # path('team-assignment/', TeamAssignmentList.as_view(), name='task-list'),
]