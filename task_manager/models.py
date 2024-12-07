import datetime
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_member = models.BooleanField(
        default=False,
        help_text="Can access the app",
    )
    is_admin = models.BooleanField(default=False, help_text="Can access the admin part of the app to manage tasks")


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    junior_factor = models.FloatField(default=2.0)
    senior_factor = models.FloatField(default=0.8)

    def __str__(self):
        return self.title


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

    class Meta:
        unique_together = ("user", "category")

    def __str__(self):
        return f"{self.user.username} assigned to {self.category.title} with level {self.level}"


class ScheduleRule(models.Model):
    """
    Defines recurring schedule rules for a user.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="schedule_rules")
    day_of_week = models.IntegerField(
        choices=[
            (0, "Monday"),
            (1, "Tuesday"),
            (2, "Wednesday"),
            (3, "Thursday"),
            (4, "Friday"),
            (5, "Saturday"),
            (6, "Sunday"),
        ],
        help_text="Day of the week (0=Monday, 6=Sunday)",
    )
    factor = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Work factor for this day (e.g., 0.0 for no work, 0.5 for half-time, 1.0 for full-time)",
    )
    start_date = models.DateField(null=True, blank=True, help_text="Optional start date for the rule")
    end_date = models.DateField(null=True, blank=True, help_text="Optional end date for the rule")

    class Meta:
        unique_together = ("user", "day_of_week", "start_date", "end_date")
        verbose_name = "Schedule Rule"
        verbose_name_plural = "Schedule Rules"

    def __str__(self):
        return f"{self.user.username}: {self.get_day_of_week_display()} - {self.factor}"


class ScheduleOverride(models.Model):
    """
    Defines exceptions to the regular schedule for a specific user and date.
    """

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="schedule_overrides")
    date = models.DateField(help_text="Specific date for the override")
    factor = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        help_text="Override work factor for this date (e.g., 0.0 for no work, 1.0 for full-time)",
    )

    class Meta:
        unique_together = ("user", "date")
        verbose_name = "Schedule Override"
        verbose_name_plural = "Schedule Overrides"

    def __str__(self):
        return f"{self.user.username}: {self.date} - {self.factor}"


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20)
    active_state = models.BooleanField(default=True, help_text="An active status will be used to filter active tasks")

    def __str__(self):
        return self.status


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    status = models.ForeignKey(Status, null=True, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    picked_at = models.DateTimeField(auto_now_add=False, null=True)
    estimated_duration = models.DurationField(default=datetime.timedelta(days=1))
    expected_finalization = models.DateTimeField(auto_now_add=False, null=True)  # end date expected to finish this task
    estimated_finalization = models.DateTimeField(
        auto_now_add=False, null=True
    )  # based on the picked_at and estimated_duration
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)

    dependencies = models.ManyToManyField("self", symmetrical=False, related_name="dependent_tasks", blank=True)

    def __str__(self):
        return self.title


class TaskAudit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)


@receiver(post_save, sender=Task)
def create_task_audit(sender, instance: Task, created: Task, **kwargs):
    """
    Create a TaskAudit entry when a Task is created or its status/assigned user changes
    """
    # If it's a new task, create an audit entry
    if created:
        TaskAudit.objects.create(task=instance, status=instance.status, user=instance.assigned_user)
        return

    # For existing tasks, check if status or assigned user changed
    try:
        # Fetch the previous version of the task from the database
        previous_task = Task.objects.get(pk=instance.pk)

        # Check if status or assigned user has changed
        status_changed = previous_task.status != instance.status
        user_changed = previous_task.assigned_user != instance.assigned_user

        # Create audit entry if either status or user has changed
        if status_changed or user_changed:
            TaskAudit.objects.create(task=instance, status=instance.status, user=instance.assigned_user)
    except Task.DoesNotExist:
        # This should rarely happen, but just in case
        pass
