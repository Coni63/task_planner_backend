import datetime
import uuid
from django.db import models
from django.db.models import F, Max

from core.models.category import Category
from core.models.custom_user import CustomUser
from core.models.project import Project
from core.models.status import Status


class TaskQuerySet(models.QuerySet):
    def assign_to(self, user):
        return self.filter(picked_by=user)

    def of_project(self, project):
        return self.filter(project=project)

    def in_status(self, status):
        return self.filter(status__state__in=status)

    def sorted(self):
        return self.order_by(F("order").asc(nulls_last=True), "created_at")

    def in_state(self, state):
        return self.filter(status__state=state)

    def in_categories(self, categories):
        return self.filter(category__in=categories)


class TaskManager(models.Manager):
    def get_queryset(self):
        return TaskQuerySet(self.model, using=self._db)

    def create_task(self, **kwargs):
        max_order = (
            Task.objects.filter(status__state__in=["active", "pending", "blocked"])
            .exclude(order__isnull=True)
            .aggregate(max_order=Max("order"))["max_order"]
        )
        kwargs["order"] = max_order + 10 if max_order else 10

        return self.create(**kwargs)

    def get_user_active_tasks(self, user):
        return self.get_queryset().assign_to(user).in_state("active")

    def pick_next_task(self, user, categories):
        next_task = self.get_queryset().in_categories(categories).in_state("pending").order_by("order").first()

        if not next_task:
            return None

        next_task.picked_by = user
        next_task.picked_at = datetime.datetime.now(datetime.timezone.utc)
        next_task.status = Status.objects.get(status="In Progress")
        next_task.save()

        return next_task


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    reference = models.CharField(max_length=64, null=False, unique=False, default="ABC-1234")
    reference_link = models.URLField(null=True)
    comments = models.TextField(null=True, max_length=1000)
    status = models.ForeignKey(Status, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    picked_by = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE, related_name="picked_by")
    picked_at = models.DateTimeField(auto_now_add=False, null=True)
    estimated_duration = models.DurationField(default=datetime.timedelta(days=1))
    expected_finalization = models.DateTimeField(auto_now_add=False, null=True)  # end date expected to finish this task
    estimated_picked_at = models.DateTimeField(auto_now_add=False, null=True)
    estimated_finalization = models.DateTimeField(auto_now_add=False, null=True)  # end date planned to finish this task
    reserved_for_user = models.ForeignKey(
        CustomUser, null=True, on_delete=models.CASCADE, related_name="reserved_for_user"
    )
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    order = models.FloatField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    dependencies = models.ManyToManyField("self", symmetrical=False, related_name="dependent_tasks", blank=True)

    objects: TaskManager = TaskManager()

    class Meta:
        permissions = [("pick_task", "The user is allowed to pick a new task")]

    def __str__(self):
        return f"Task({self.reference}, status={self.status}, project={self.project}, picked_by={self.picked_by})"
