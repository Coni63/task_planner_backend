
import uuid
from django.db import models


class Status(models.Model):

    class States(models.TextChoices):
        PENDING = 'pending'
        ACTIVE = 'active'
        CLOSED = 'closed'
        BLOCKED = 'blocked'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20)
    state = models.CharField(
        max_length=10,
        choices=States.choices,
        default=States.BLOCKED,
    )
    color = models.CharField(max_length=7, default="#FFFFFF")
    dark_color = models.CharField(max_length=7, default="#000000")

    def __str__(self):
        return self.status
