from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    name = models.CharField(max_length=255)
    managers = models.ManyToManyField(User, related_name="managed_teams")
    members = models.ManyToManyField(User, through="TeamAssignment", related_name="teams")

    def __str__(self):
        return self.name


class Category(models.Model):
    title = models.CharField(max_length=255)
    junior_factor = models.FloatField()
    senior_factor = models.FloatField()

    def __str__(self):
        return self.title
    

class TeamAssignment(models.Model):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("member", "Member"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    class Meta:
        unique_together = ("user", "team")

    def __str__(self):
        return f"{self.user.username} ({self.role}) in {self.team.name}"
    

class UserAssignment(models.Model):
    ROLE_CHOICES = [
        ("Blocked", "Blocked"),
        ("Junior", "Junior"),
        ("Medior", "Medior"),
        ("Senior", "Senior"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    level = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} assigned to {self.category.title} with level {self.level}"



class Task(models.Model):
    title = models.CharField(max_length=255)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
