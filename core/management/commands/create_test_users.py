from django.core.management.base import BaseCommand
from core.models import Category, CustomUser, Project, Status
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):
        self.create_groups()
        self.create_users()
        self.create_categories()
        self.create_statuses()
        self.create_projects()

    def create_groups(self):
        groups = ['ADMIN', 'COORDINATOR', 'MANAGER', 'MEMBER']
        
        for group_name in groups:
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f'Created group "{group_name}"')
            else:
                self.stdout.write(f'Group "{group_name}" already exists')

    def create_users(self):
        for i in range(0, 5):
            if i == 0:
                username = "admin"
            else:
                username = f"user{i}"
            password = "password"

            user, created = CustomUser.objects.get_or_create(username=username, email=f"{username}@example.com")
            if created:
                user.set_password(password)
                if i == 0:
                    user.is_admin = True
                    user.is_member = True
                    user.is_superuser = True
                    user.is_staff = True
                    admin_group = Group.objects.get(name='ADMIN')
                    user.groups.add(admin_group)
                elif i == 1:
                    user.is_member = True
                    user.is_admin = False
                    member_group = Group.objects.get(name='MEMBER')
                    user.groups.add(member_group)
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created user: {username} with password: {password}"))
            else:
                self.stdout.write(self.style.WARNING(f"User {username} already exists"))

    def create_categories(self):
        for i in range(1, 4):
            title = f"Category{i}"
            junior_factor = 2.0
            senior_factor = 0.8
            category, created = Category.objects.get_or_create(
                title=title, junior_factor=junior_factor, senior_factor=senior_factor
            )
            if created:
                category.save()
                self.stdout.write(self.style.SUCCESS(f"Category created: {title}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category {title} already exists"))

    def create_statuses(self):
        data = [
            ("To Do", "pending"),
            ("In Progress", "active"),
            ("In Review", "active"),
            ("Done", "closed"),
            ("On Hold", "blocked"),
            ("Cancelled", "closed"),
            ("Not Ready", "blocked"),
        ]
        for status, state in data:
            status, created = Status.objects.get_or_create(status=status, state=state)
            if created:
                status.save()
                self.stdout.write(self.style.SUCCESS(f"Status created: {status}"))
            else:
                self.stdout.write(self.style.WARNING(f"Status {status} already exists"))

    def create_projects(self):
        for i in range(1, 3):
            name = f"Project{i}"
            description = f"Project {i} description"
            trigram = f"PR{i}"
            project, created = Project.objects.get_or_create(name=name, description=description, trigram=trigram)
            if created:
                project.save()
                self.stdout.write(self.style.SUCCESS(f"Project created: {name} {description}"))
            else:
                self.stdout.write(self.style.WARNING(f"Project {name} {description} already exists"))
