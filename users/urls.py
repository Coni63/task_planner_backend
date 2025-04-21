import uuid
from django.urls import include, path, register_converter
from . import views

class UUIDConverter:
    regex = "[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"

    def to_python(self, value):
        return uuid.UUID(value)

    def to_url(self, value):
        return str(value)


register_converter(UUIDConverter, "uuid")

urlpatterns = [
    path('profile/<uuid:pk>/', views.profile, name='profile'),
]