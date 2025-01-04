import uuid

from core.models import Task, UserAssignment
from core.serializers.task_serializer import TaskSerializer, TaskSimpleSerializer
from optimization.optimizer import GeneticAlgorithm

def optimize(data):
    tasks: dict[uuid.UUID, Task] = {}  # task_id -> Task
    for task in Task.objects.exclude(status__state__in=['closed', 'blocked']):
        tasks[task.id] = task

    factors: dict[uuid.UUID, dict[uuid.UUID, float]] = {}  # user_id -> category_id -> factor
    for skill in UserAssignment.objects.all().prefetch_related('category'):
        if skill.user.id not in factors:
            factors[skill.user.id] = {}

        if skill.level == 'Junior':
            factors[skill.user.id][skill.category.id] = skill.category.junior_factor
        elif skill.level == 'Medior':
            factors[skill.user.id][skill.category.id] = 1.0
        elif skill.level == 'Senior':
            factors[skill.user.id][skill.category.id] = skill.category.senior_factor

    task_user_map = {}  # user_id -> task_id -> factor
    for user in factors:
        task_user_map[user] = {}
        for task_id, task in tasks.items():
            if task.category.id not in factors[user]:
                continue
            task_user_map[user][task_id] = factors[user][task.category.id]

    solver = GeneticAlgorithm(tasks, task_user_map)
    solution = solver.run(generations=100)

    patch_tasks(solution)
    


def check_dependencies(data):
    def dfs(task_id: str, visited: set[str], recursion_stack: set[str]):
        if task_id in recursion_stack:
            raise ValueError(f"Cyclic dependency detected at task ID {task_id}")
        
        if task_id in visited:
            return
        
        visited.add(task_id)
        recursion_stack.add(task_id)
        for dep_id in task_graph.get(task_id, []):
            dfs(dep_id, visited, recursion_stack)
        recursion_stack.remove(task_id)
    
    project = data.get("project")
    if not project:
        raise ValueError("Project is required.")
    project = uuid.UUID(project)

    root_task = data.get("base_task")
    if not root_task:
        raise ValueError("A base task is required.")
    root_task = uuid.UUID(root_task)

    # Build the task graph
    task_graph = {}
    tasks = Task.objects.filter(project=project).prefetch_related("dependencies")
    for task in tasks:
        task_graph[task.id] = [dep.id for dep in task.dependencies.all()]

    # Check if the base tasks are in the graph
    if root_task not in task_graph:
        raise ValueError("Base task not found in the project.")
    
    # Check all root tasks for cycles
    visited = set()
    recursion_stack = set()
    dfs(root_task, visited, recursion_stack)

    return



from rest_framework.exceptions import ValidationError

def patch_tasks(data: list[dict]):
    """
    Patch tasks based on a list of dictionaries.
    Each dictionary should have keys 'id', 'order', and 'reservedForUser'.
    """
    for item in data:
        try:
            task = Task.objects.get(id=item["id"])
            serializer = TaskSimpleSerializer(
                task,
                data=item,
                partial=True,
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        except Task.DoesNotExist:
            raise ValidationError({"error": f"Task with id {item['id']} not found."})