import uuid
from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    junior_factor = models.FloatField(default=2.0)
    senior_factor = models.FloatField(default=0.8)

    def __str__(self):
        return self.title
    

class TeamAssignment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user_id", "team_id")

    def __str__(self):
        return f"{self.user_id} assigned in {self.team_id}"
    

class UserAssignment(models.Model):
    ROLE_CHOICES = [
        ("Blocked", "Blocked"),
        ("Junior", "Junior"),
        ("Medior", "Medior"),
        ("Senior", "Senior"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, default="Blocked", choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user_id.username} assigned to {self.category_id.title} with level {self.level}"


class ScheduleRule(models.Model):
    """
    Defines recurring schedule rules for a user.
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_rules')
    day_of_week = models.IntegerField(
        choices=[
            (0, 'Monday'),
            (1, 'Tuesday'),
            (2, 'Wednesday'),
            (3, 'Thursday'),
            (4, 'Friday'),
            (5, 'Saturday'),
            (6, 'Sunday'),
        ],
        help_text="Day of the week (0=Monday, 6=Sunday)"
    )
    factor = models.DecimalField(
        max_digits=3, decimal_places=2,
        help_text="Work factor for this day (e.g., 0.0 for no work, 0.5 for half-time, 1.0 for full-time)"
    )
    start_date = models.DateField(
        null=True, blank=True,
        help_text="Optional start date for the rule"
    )
    end_date = models.DateField(
        null=True, blank=True,
        help_text="Optional end date for the rule"
    )

    class Meta:
        unique_together = ('user_id', 'day_of_week', 'start_date', 'end_date')
        verbose_name = "Schedule Rule"
        verbose_name_plural = "Schedule Rules"

    def __str__(self):
        return f"{self.user_id.username}: {self.get_day_of_week_display()} - {self.factor}"


class ScheduleOverride(models.Model):
    """
    Defines exceptions to the regular schedule for a specific user and date.
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='schedule_overrides')
    date = models.DateField(help_text="Specific date for the override")
    factor = models.DecimalField(
        max_digits=3, decimal_places=2,
        help_text="Override work factor for this date (e.g., 0.0 for no work, 1.0 for full-time)"
    )

    class Meta:
        unique_together = ('user_id', 'date')
        verbose_name = "Schedule Override"
        verbose_name_plural = "Schedule Overrides"

    def __str__(self):
        return f"{self.user_id.username}: {self.date} - {self.factor}"


class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(max_length=20)

    def __str__(self):
        return self.status
    

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True)
    status_id = models.ForeignKey(Status, null=True, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    assigned_user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    picked_at = models.DateTimeField(auto_now_add=False, null=True)
    estimated_duration = models.DurationField(default=0)
    expected_finalization = models.DateTimeField(auto_now_add=False, null=True)  # end date expected to finish this task
    estimated_finalization = models.DateTimeField(auto_now_add=False, null=True) # based on the picked_at and estimated_duration
    category_id = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    
    dependencies = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='dependent_tasks',
        blank=True
    )

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Check if the object already exists in the database
        if self.pk:
            old_task = Task.objects.get(pk=self.pk)
            if (
                old_task.status_id != self.status_id
                or old_task.assigned_user_id != self.assigned_user_id
            ):
                # Insert an audit entry
                TaskAudit.objects.create(
                    task_id=self,
                    status_id=self.status_id,
                    user_id=self.assigned_user_id
                )
        super().save(*args, **kwargs)
    

class TaskAudit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    status_id = models.ForeignKey(Status, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)