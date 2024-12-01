from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from task_manager.models import Team

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_teams()

    
    def create_users(self):
        for i in range(1, 11):
            username = f"user{i}"
            password = "password"
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {username} with password: {password}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {username} already exists"))
    
    def create_teams(self):
        for i in range(1, 3):
            name = f"Team{i}"
            team, created = Team.objects.get_or_create(name=name)
            if created:
                team.save()
                self.stdout.write(self.style.SUCCESS(f"Team created: {name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Team {name} already exists"))