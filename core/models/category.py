import uuid
from django.db import models



class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    junior_factor = models.FloatField(default=2.0)
    senior_factor = models.FloatField(default=0.8)

    def __str__(self):
        return self.title
