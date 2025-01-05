from collections import defaultdict
from dataclasses import dataclass
import dataclasses
import datetime
import random
import uuid

from core.models import Task


def topological_sort(tasks: dict[uuid.UUID, Task]) -> list[uuid.UUID]:
    """
    Performs topological sort on tasks based on dependencies.
    Returns list of list of task IDs in execution order. Each list represents a depth level.

    :param tasks: Dictionary of task IDs and corresponding Task objects
    :return: List of task IDs in topological order
    """
    # Step 1: Build the in-degree map and adjacency list
    in_degree = {task_id: 0 for task_id in tasks}
    adjacency_list = {task_id: [] for task_id in tasks}

    for task in tasks.values():
        for dependency in task.dependencies.all():
            if dependency.id in tasks:
                in_degree[task.id] += 1
                adjacency_list[dependency.id].append(task.id)

    # Step 2: Find all nodes with in-degree 0
    zero_in_degree_queue = [task_id for task_id, degree in in_degree.items() if degree == 0]

    # Step 3: Assign depths using a BFS approach
    depth_map = {task_id: 0 for task_id in tasks}
    while zero_in_degree_queue:
        current = zero_in_degree_queue.pop(0)
        current_depth = depth_map[current]

        for neighbor in adjacency_list[current]:
            in_degree[neighbor] -= 1
            # Update the depth of the neighbor
            depth_map[neighbor] = max(depth_map[neighbor], current_depth + 1)
            if in_degree[neighbor] == 0:
                zero_in_degree_queue.append(neighbor)

    # Step 4: Organize tasks by depth
    max_depth = max(depth_map.values())
    depth_groups = [[] for _ in range(max_depth + 1)]
    for task_id, depth in depth_map.items():
        depth_groups[depth].append(task_id)

    return depth_groups


@dataclass
class Gene:
    task_id: uuid.UUID
    user_id: uuid.UUID
    factor: float
    estimated_picked_at: datetime.datetime | None = None
    estimated_finalization: datetime.datetime | None = None

@dataclass
class Chromosome:
    genes: list[Gene]
    fitness: datetime.datetime | None = None

    def __repr__(self):
        return f"Chromosome(genes=[...], fitness={self.fitness})"

    def to_json(self) -> dict:
        return [
            {
                "order": order,
                "id": gene.task_id, 
                "reserved_for_user": gene.user_id,
                "estimated_finalization": gene.estimated_finalization,
                "estimated_picked_at": gene.estimated_picked_at,
            } 
            for order, gene in enumerate(self.genes, start=1)
        ]

class GeneticAlgorithm:
    def __init__(self, tasks: dict[uuid.UUID, Task], task_user_map: dict[uuid.UUID, dict[uuid.UUID, float]]):
        self.tasks = tasks                                # map task_id -> Task
        self.task_user_map = task_user_map                # map user_id -> task_id -> factor
        self.task_depth_groups = topological_sort(tasks)  # List of list of task IDs grouped by depth

        assert self.all_tasks_have_users(), "All tasks must have at least one user able to do it."

    def run(self, *, population_size: int = 10, generations: int = 50, mutation_rate: float = 0.1) -> dict:
        population = self._initialize_population(population_size)
        for generation in range(generations):
            print(f"Generation {generation+1}/{generations}")

            population = self._selection(population, population_size)
            while len(population) < population_size:
                child = self._random_chromosome()
                population.append(child)

                parent1, parent2 = random.sample(population, 2)
                population.extend(self._crossover(parent1, parent2))

                if random.random() < mutation_rate:
                    parent = random.choice(population)
                    mutated = self._mutate(parent)
                    if mutated is not None:
                        population.append(self._mutate(parent))
            
            print(f"Best fitness: {min(population, key=lambda x: x.fitness).fitness}")

        winner = min(population, key=lambda x: x.fitness)
        winner.genes.sort(key=lambda x: x.estimated_finalization)
        return winner.to_json()


    def _initialize_population(self, population_size) -> list[Chromosome]:
        population = []
        for _ in range(population_size):
            c = self._random_chromosome()
            population.append(c)
        return population
    
    def _random_chromosome(self) -> Chromosome:
        chromosome = []
        for task_group in self.task_depth_groups:
            random.shuffle(task_group)
            for task_id in task_group:
                possible_users = [user_id for user_id in self.task_user_map if task_id in self.task_user_map[user_id]]
                user_id = random.choice(possible_users)
                factor = self.task_user_map[user_id][task_id]
                chromosome.append(Gene(task_id=task_id, user_id=user_id, factor=factor))
        c = Chromosome(chromosome)
        self._calculate_fitness(c)
        return c

    def _selection(self, population: list[Chromosome], population_size: int) -> list[Chromosome]:
        population.sort(key=lambda x: x.fitness)
        return population[:population_size // 2]
    
    def _crossover(self, parent1: Chromosome, parent2: Chromosome) -> list[Chromosome]:
        swapped_depths = random.randint(0, len(self.task_depth_groups)-1)
        idx1 = sum(len(group) for group in self.task_depth_groups[:swapped_depths])
        idx2 = idx1 + len(self.task_depth_groups[swapped_depths])

        child1 = parent1.genes[:idx1] + parent2.genes[idx1:idx2] + parent1.genes[idx2:]
        child2 = parent2.genes[:idx1] + parent1.genes[idx1:idx2] + parent2.genes[idx2:]
        
        c1 = Chromosome(child1)
        c2 = Chromosome(child2)
        self._calculate_fitness(c1)
        self._calculate_fitness(c2)
        return [c1, c2]
    
    def _mutate(self, parent: Chromosome) -> Chromosome:
        child = dataclasses.replace(parent)  # Copy the parent chromosome
        
        tries = 0
        while tries < 10:
            case = random.randint(0, 2)
            if case == 0:
                # Change user
                gene_idx = random.randint(0, len(child.genes)-1)
                initial_gene = child.genes[gene_idx]
                possible_users = [user_id for user_id in self.task_user_map if initial_gene.task_id in self.task_user_map[user_id] and user_id != initial_gene.user_id]
                if len(possible_users) > 0:
                    user_id = random.choice(possible_users)
                    factor = self.task_user_map[user_id][initial_gene.task_id]
                    child.genes[gene_idx] = Gene(task_id=initial_gene.task_id, user_id=user_id, factor=factor)
                    self._calculate_fitness(child)
                    return child
            else:
                # Swap genes
                possible_depths = [i for i in range(len(self.task_depth_groups)) if len(self.task_depth_groups[i]) > 1]
                if len(possible_depths) > 0:
                    swapped_depths = random.choice(possible_depths)
                    start = sum(len(group) for group in self.task_depth_groups[:swapped_depths])
                    end = start + len(self.task_depth_groups[swapped_depths])

                    idx1, idx2 = random.sample(range(start, end), 2)
                    child.genes[idx1], child.genes[idx2] = child.genes[idx2], child.genes[idx1]
                    self._calculate_fitness(child)
                    return child
            tries += 1
        return None


    def _calculate_fitness(self, chromosome: Chromosome) -> float:
        user_end_times: dict[uuid.UUID, datetime.datetime] = {}
        task_end_times: dict[uuid.UUID, datetime.datetime] = {}

        for gene in chromosome.genes:
            if gene.user_id not in user_end_times:
                user_end_times[gene.user_id] = datetime.datetime.now(tz=datetime.timezone.utc)

            task = self.tasks[gene.task_id]
            duration = task.estimated_duration * gene.factor

            start_task = user_end_times[gene.user_id]
            for dep in task.dependencies.all():
                start_task = max(start_task, task_end_times[dep.id])

            end_time = start_task + duration
            user_end_times[gene.user_id] = end_time
            task_end_times[task.id] = end_time
            
            gene.estimated_picked_at = start_task
            gene.estimated_finalization = end_time
        
        chromosome.fitness = max(task_end_times.values())

    
    def __get_same_depth_tasks(self, task: uuid.UUID) -> list[uuid.UUID]:
        for group in self.task_depth_groups:
            if task in group:
                return group
        return []
    
    def all_tasks_have_users(self) -> bool:
        for task in self.tasks.values():
            if not any(task.id in user_tasks for user_tasks in self.task_user_map.values()):
                return False
        return True
    
