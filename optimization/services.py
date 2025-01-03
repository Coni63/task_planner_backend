from collections import defaultdict
import datetime
import random
import time
import uuid

from core.models import Task, UserAssignment

class Chromosome:
    def __init__(self, genes: list[dict], tasks: dict[uuid.UUID, Task], task_user_map: dict[uuid.UUID, dict[uuid.UUID, float]]):
        self.genes = genes
        self.tasks = tasks
        self.task_user_map = task_user_map
        self._fitness = None

    @property
    def fitness(self) -> float:
        if self._fitness is None:
            self._fitness = self._calculate_fitness()
        return self._fitness
    
    def crossover(self, other: 'Chromosome') -> 'Chromosome':
        # TODO: Attention to duplicate tasks
        split_point = len(self.genes) // 2
        child1 = self.genes[:split_point] + other.genes[split_point:]
        child2 = other.genes[:split_point] + self.genes[split_point:]
        return [Chromosome(child1, self.tasks, self.task_user_map), Chromosome(child2, self.tasks, self.task_user_map)]
    
    def mutate(self) -> 'Chromosome':
        new_genes = self.genes[:]
        gene = random.choice(new_genes)
        possible_users = [user_id for user_id, possible_tasks in self.task_user_map.items() if gene["task_id"] in possible_tasks]
        gene["user_id"] = random.choice(possible_users)
        gene["factor"] = self.task_user_map[gene["user_id"]][gene["task_id"]]
        return Chromosome(new_genes, self.tasks, self.task_user_map)

    def _calculate_fitness(self) -> float:
        makespan = datetime.datetime.now(tz=datetime.timezone.utc)
        user_end_times = defaultdict(datetime.datetime)
        dependency_end_times = defaultdict(datetime.datetime)

        for gene in sorted(self.genes, key=lambda x: x["order"]):
            task = self.tasks[gene["task_id"]]
            user = gene["user_id"]

            dependancies = task.dependencies.all()
            if dependancies:
                start_time = max(
                    user_end_times.get(user, datetime.datetime.now(tz=datetime.timezone.utc)),
                    max(dependency_end_times.get(dep, datetime.datetime.now(tz=datetime.timezone.utc)) for dep in task.dependencies.all())
                )
            else:
                start_time = user_end_times.get(user, datetime.datetime.now(tz=datetime.timezone.utc))

            duration = task.estimated_duration * gene["factor"]
            end_time = start_time + duration
            user_end_times[user] = end_time
            dependency_end_times[task.id] = end_time
            makespan = max(makespan, end_time)

        return makespan

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

        
    # Genetic Algorithm Setup
    POPULATION_SIZE = 10
    GENERATIONS = 50
    MUTATION_RATE = 0.1

    # Initialize population
    def initialize_population(tasks: dict[uuid.UUID, Task], task_user_map: dict[uuid.UUID, dict[uuid.UUID, float]]) -> list[Chromosome]:
        population = []
        for _ in range(POPULATION_SIZE):
            chromosome = []

            orders = list(range(len(tasks)))
            random.shuffle(orders)
            for task_id, order in zip(tasks, orders):
                possible_users = [user_id for user_id in task_user_map if task_id in task_user_map[user_id]]
                if not possible_users:
                    raise ValueError(f"No users found for task ID {task_id}")
                user_id = random.choice(possible_users)
                factor = task_user_map[user_id][task_id]
                chromosome.append({"task_id": task_id, "user_id": user_id, "order": order, "factor": factor})
            population.append(Chromosome(chromosome, tasks, task_user_map))
        return population

    # Selection
    def selection(population: list[Chromosome]) -> list[Chromosome]:
        population.sort(key=lambda x: x.fitness)
        return population[:POPULATION_SIZE // 2]

    # Main GA Loop
    def genetic_algorithm(tasks: dict[uuid.UUID, Task], task_user_map: dict[uuid.UUID, dict[uuid.UUID, float]]):
        population = initialize_population(tasks, task_user_map)
        for generation in range(GENERATIONS):
            print(f"Generation {generation+1}/{GENERATIONS}")
            
            next_generation = selection(population)
            
            while len(next_generation) < POPULATION_SIZE:
                parent1, parent2 = random.sample(next_generation, 2)
                next_generation.extend(parent1.crossover(parent2))

                if random.random() < MUTATION_RATE:
                    parent1 = random.choice(next_generation)
                    next_generation.append(parent1.mutate())
        
            population = next_generation
            print("Best Fitness", min(population, key=lambda x: x.fitness).fitness)

        best_solution = min(population, key=lambda x: x.fitness)
        return best_solution

    # Run GA
    best_solution = genetic_algorithm(tasks, task_user_map)
    print("Optimized Task Assignment:", best_solution)

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