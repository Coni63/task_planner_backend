import uuid
from django.db import models

from core.models.custom_user import CustomUser


class ScheduleRule(models.Model):
    """
    Defines recurring schedule rules for a user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
