from enum import Enum
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class Role(Enum):
    ADMIN = 'Administrator'
    VISITOR = 'Visitor'
    USER = 'User'
    
    @classmethod
    def choices(cls):
        return [(item.value, item.name) for item in cls]


# Create your models here.
class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    role = models.CharField(
        choices=Role.choices(),
        default=Role.VISITOR.value,
        max_length=32,
    )

    @property
    def get_avatar(self):
        print
        if self.avatar:
            return self.avatar.url
        return 'https://placehold.co/80x80'  # fallback