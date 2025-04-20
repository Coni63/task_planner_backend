from django.urls import include, path
from . import views

urlpatterns = [
    path('profile/', views.my_profile, name='my-profile'),
]