import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.URLField(null=True, blank=True)
    categories = models.ManyToManyField("Category", through="UserAssignment")

    class Meta:
        permissions = [
            ("change_someone_else_user", "Can update another user's profile"),
            ("delete_someone_else_user", "Can delete another user's profile"),
        ]
