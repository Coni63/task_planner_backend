import datetime
from django.core.management.base import BaseCommand
from task_manager.models import Category, CustomUser, Project, ScheduleRule, Status, Task, UserAssignment


class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):
        self.create_users()
        self.create_categories()
        self.create_statuses()

        self.create_user_assignments()

        self.create_projects()
        # self.create_tasks()

        self.set_dayoff()

    def create_users(self):
        for i in range(0, 11):
            if i == 0:
                username = "admin"
            else:
                username = f"user{i}"
            password = "password"

            user, created = CustomUser.objects.get_or_create(username=username, email=f"{username}@example.com")
            if created:
                user.set_password(password)
                if i == 0:
                    user.is_superuser = True
                    user.is_staff = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {username} with password: {password}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {username} already exists"))

    def create_categories(self):
        for i in range(1, 4):
            title = f"Category{i}"
            junior_factor = 1.2
            senior_factor = 1.5
            category, created = Category.objects.get_or_create(
                title=title, junior_factor=junior_factor, senior_factor=senior_factor
            )
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
            user = CustomUser.objects.get(username=f"user{i}")
            category = Category.objects.get(title="Category1")
            level = "Junior"
            user_assignment, created = UserAssignment.objects.get_or_create(user=user, category=category, level=level)
            if created:
                user_assignment.save()
                self.stdout.write(self.style.SUCCESS(f"UserAssignment created: {user} {category} {level}"))
            else:
                self.stdout.write(self.style.WARNING(f"UserAssignment {user} {category} {level} already exists"))

    def create_projects(self):
        for i in range(1, 3):
            name = f"Project{i}"
            description = f"Project {i} description"
            project, created = Project.objects.get_or_create(name=name, description=description)
            if created:
                project.save()
                self.stdout.write(self.style.SUCCESS(f"Project created: {name} {description}"))
            else:
                self.stdout.write(self.style.WARNING(f"Project {name} {description} already exists"))

    def create_tasks(self):
        project = Project.objects.get(name="Project1")
        status = Status.objects.get(status="Status1")
        category = Category.objects.get(title="Category1")
        for i in range(1, 20):
            titre = f"Task{i}"
            description = f"Task {i} description"

            if i == 1:
                assigned_user = CustomUser.objects.get(username="user1")
                picked_at = datetime.datetime.now(datetime.timezone.utc)
            else:
                assigned_user = None
                picked_at = None

            estimated_duration = datetime.timedelta(days=i)
            expected_finalization = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=i + 5)
            estimated_finalization = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=i)

            task, created = Task.objects.get_or_create(
                title=titre,
                description=description,
                status=status,
                category=category,
                project=project,
                assigned_user=assigned_user,
                picked_at=picked_at,
                estimated_duration=estimated_duration,
                expected_finalization=expected_finalization,
                estimated_finalization=estimated_finalization,
            )

            if created:
                task.save()
                self.stdout.write(self.style.SUCCESS(f"Task created: {titre} created"))
            else:
                self.stdout.write(self.style.WARNING(f"Task {titre} already exists"))

    def set_dayoff(self):
        for userid in range(0, 11):
            if userid == 0:
                username = "admin"
            else:
                username = f"user{userid}"
            user = CustomUser.objects.get(username=username)

            av_sat, created_sat = ScheduleRule.objects.get_or_create(user=user, day_of_week=5, factor=0.0)
            av_sun, created_sun = ScheduleRule.objects.get_or_create(user=user, day_of_week=6, factor=0.0)

            if created_sat and created_sun:
                av_sat.save()
                av_sun.save()
                self.stdout.write(self.style.SUCCESS(f"UserAvailability created: {user.username}"))
            else:
                self.stdout.write(self.style.WARNING(f"UserAvailability {user.username} already exists"))
