import random
import datetime
from django.core.management.base import BaseCommand
from core.models import Category, CustomUser, Project, Status, Task, WorkflowTransition
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = "Generate test data"

    def handle(self, *args, **kwargs):
        self.create_groups()
        self.create_users()
        self.create_categories()
        self.create_statuses()
        self.create_workflow_transitions()
        self.create_projects()
        self.create_tasks()

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
                    user.is_superuser = True
                    user.is_staff = True
                    admin_group = Group.objects.get(name='ADMIN')
                    user.groups.add(admin_group)
                elif i == 1:
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

    def create_workflow_transitions(self):
        data = [
            ("To Do", "In Progress"),
            ("To Do", "On Hold"),
            ("To Do", "Not Ready"),
            ("To Do", "Cancelled"),
            ("In Progress", "To Do"),
            ("In Progress", "In Review"),
            ("In Progress", "Done"),
            ("In Progress", "On Hold"),
            ("In Progress", "Cancelled"),
            ("In Review", "Done"),
            ("In Review", "In Progress"),
            ("In Review", "On Hold"),
            ("In Review", "Cancelled"),
            ("On Hold", "To Do"),
            ("On Hold", "In Progress"),
            ("On Hold", "In Review"),
            ("On Hold", "Done"),
            ("On Hold", "Cancelled"),
            ("Not Ready", "To Do"),
            ("Not Ready", "In Progress"),
        ]

        for from_status, to_status in data:
            from_status = Status.objects.get(status=from_status)
            to_status = Status.objects.get(status=to_status)
            transition, created = WorkflowTransition.objects.get_or_create(
                from_status=from_status, to_status=to_status
            )
            if created:
                transition.save()
                self.stdout.write(self.style.SUCCESS(f"Transition created: {from_status} -> {to_status}"))
            else:
                self.stdout.write(self.style.WARNING(f"Transition {from_status} -> {to_status} already exists"))

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

    def create_tasks(self):
        # Retrieve or create example statuses, projects, and categories
        status = Status.objects.filter(status="To Do").first()
        project = Project.objects.filter(name="Project1").first()
        categories = list(Category.objects.all())

        # Clear existing tasks for a clean slate
        Task.objects.all().delete()

        # Generate tasks
        task_references: list[Task] = []
        for i in range(20):
            reference = f"ABC-{str(i+1).zfill(4)}"
            comments = f"This is a sample comment for task {reference}."
            category = random.choice(categories)
            estimated_duration = datetime.timedelta(days=random.randint(1, 10), hours=random.randint(0, 23))
            expected_finalization = datetime.datetime.now(tz=datetime.timezone.utc) + estimated_duration

            # Create the task
            task = Task.objects.create(
                reference=reference,
                comments=comments,
                status=status,
                project=project,
                estimated_duration=estimated_duration,
                expected_finalization=expected_finalization,
                category=category
            )

            task_references.append(task)

            # Add dependencies
            num_dependencies = random.randint(0, min(2, len(task_references)-1))
            dependencies = random.sample(task_references[:-1], num_dependencies)

            for dep in dependencies:
                task.dependencies.add(dep)
            
            self.stdout.write(self.style.SUCCESS(f"Successfully create a task - {len(dependencies)} dependancies"))
