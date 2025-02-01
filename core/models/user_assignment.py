import uuid
from django.db import models
from django.db.models import Q, F, Max
from core.models.custom_user import CustomUser
from core.models.category import Category

class UserAssignmentQuerySet(models.QuerySet):
    def assign_to(self, user):
        return self.filter(user = user)
    
    def not_blocked(self):
        return self.filter(~Q(level="Blocked"))


class UserAssignmentManager(models.Manager):
    def get_queryset(self):
        return UserAssignmentQuerySet(self.model, using=self._db)

    def get_user_assignments(self, user):
        return self.get_queryset().assign_to(user).not_blocked().values_list('category', flat=True)

class UserAssignment(models.Model):
    ROLE_CHOICES = [
        ("Blocked", "Blocked"),
        ("Junior", "Junior"),
        ("Medior", "Medior"),
        ("Senior", "Senior"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, default="Blocked", choices=ROLE_CHOICES)

    objects: UserAssignmentManager = UserAssignmentManager()

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"({self.user.username}, {self.category.title}, {self.level})"

