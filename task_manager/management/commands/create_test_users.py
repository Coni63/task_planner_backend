import datetime
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from task_manager.models import Category, Project, Status, Task, Team, TeamAssignment, UserAssignment

class Command(BaseCommand):
    help = 'Generate test data'

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_teams()
        self.create_categories()
        self.create_statuses()

        self.create_user_assignments()
        self.create_team_assignments()

        self.create_projects()
        self.create_tasks()

    
    def create_users(self):
        for i in range(0, 11):
            if i == 0:
                username = "admin"
            else:
                username = f"user{i}"
            password = "password"

            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                if i == 0:
                    user.is_superuser = True
                    user.is_staff = True
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

    def create_categories(self):
        for i in range(1, 4):
            title = f"Category{i}"
            junior_factor = 1.2
            senior_factor = 1.5
            category, created = Category.objects.get_or_create(title=title, junior_factor=junior_factor, senior_factor=senior_factor)
            if created:
                category.save()
                self.stdout.write(self.style.SUCCESS(f"Category created: {title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category {title} already exists"))

    def create_statuses(self):
        for i in range(1, 4):
            status = f"Status{i}"
            status, created = Status.objects.get_or_create(status=status)
            if created:
                status.save()
                self.stdout.write(self.style.SUCCESS(f"Status created: {status}"))
            else:
                self.stdout.write(self.style.WARNING(f"Status {status} already exists"))

    def create_user_assignments(self):
        for i in range(1, 4):
            user_id = User.objects.get(username=f"user{i}")
            category_id = Category.objects.get(title="Category1")
            level = "Junior"
            user_assignment, created = UserAssignment.objects.get_or_create(user_id=user_id, category_id=category_id, level=level)
            if created:
                user_assignment.save()
                self.stdout.write(self.style.SUCCESS(f"UserAssignment created: {user_id} {category_id} {level}"))
            else:
                self.stdout.write(self.style.WARNING(f"UserAssignment {user_id} {category_id} {level} already exists"))

    def create_team_assignments(self):
        for i in range(1, 10):
            user_id = User.objects.get(username=f"user{i}")
            team_id = Team.objects.get(name=f"Team{(i // 5) + 1}")
            is_admin = False
            is_member = True
            team_assignment, created = TeamAssignment.objects.get_or_create(user_id=user_id, team_id=team_id, is_admin=is_admin, is_member=is_member)  # noqa: F821
            if created:
                team_assignment.save()
                self.stdout.write(self.style.SUCCESS(f"TeamAssignment created: {user_id} {team_id} {is_admin} {is_member}"))
            else:
                self.stdout.write(self.style.WARNING(f"TeamAssignment {user_id} {team_id} {is_admin} {is_member} already exists"))

    def create_projects(self):
        for i in range(1, 3):
            name = f"Project{i}"
            description = f"Project {i} description"
            team_id = Team.objects.get(name=f"Team{i // 2 + 1}")
            project, created = Project.objects.get_or_create(name=name, description=description, team_id=team_id)  # noqa: F821
            if created:
                project.save()
                self.stdout.write(self.style.SUCCESS(f"Project created: {name} {description} {team_id}"))
            else:
                self.stdout.write(self.style.WARNING(f"Project {name} {description} {team_id} already exists"))

    def create_tasks(self):
        project = Project.objects.get(name="Project1")
        for i in range(1, 20):
            titre = f"Task{i}"
            description = f"Task {i} description"
            status_id = Status.objects.get(status="Status1")
            category_id = Category.objects.get(title="Category1")
            project_id = Project.objects.get(name="Project1")

            if i == 1:
                assigned_user_id = User.objects.get(username="user1")
                picked_at = datetime.datetime.now(datetime.timezone.utc)  # noqa: F821
            else:
                assigned_user_id = None
                picked_at = None
            
            estimated_duration = datetime.timedelta(days=i)
            expected_finalization = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=i + 5)
            estimated_finalization = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=i)

            task, created = Task.objects.get_or_create(
                title=titre,
                description=description,
                status_id=status_id,
                category_id=category_id,
                project_id=project_id,
                assigned_user_id=assigned_user_id,
                picked_at=picked_at,
                estimated_duration=estimated_duration,
                expected_finalization=expected_finalization,
                estimated_finalization=estimated_finalization,
            )

            if created:
                project.save()
                self.stdout.write(self.style.SUCCESS(f"Task created: {titre} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Task {titre} already exists"))

