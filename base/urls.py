from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('increment/', views.increment, name='increment'),
    path('decrement/', views.decrement, name='decrement'),
]