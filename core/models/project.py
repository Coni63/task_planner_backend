
import uuid
from django.db import models



class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    trigram = models.CharField(max_length=3, null=False, unique=True)
    order = models.IntegerField(null=True)

    def __str__(self):
        return self.name

