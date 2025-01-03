import time
import uuid

from core.models import Task

def optimize(data):
    print("Optimizing...")
    time.sleep(5)
    print("Optimization done.")
    return data

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