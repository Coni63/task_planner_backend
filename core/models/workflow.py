import uuid
from django.db import models


class WorkflowTransition(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=True, null=True)  # Optional for a name like "Standard Transition"
    from_status = models.ForeignKey("Status", related_name="transitions_from", on_delete=models.CASCADE)
    to_status = models.ForeignKey("Status", related_name="transitions_to", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.from_status.status} → {self.to_status.status}"

    class Meta:
        unique_together = ("from_status", "to_status")  # Ensure no duplicate transitions
