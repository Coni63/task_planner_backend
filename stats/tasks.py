from django.db import ProgrammingError
from django_q.models import Schedule

def compute_stats():
    print("Computing stats...")



def setup_periodic_tasks():
    try:
        Schedule.objects.update_or_create(
            name='compute_stats',
            defaults={
                'func': 'stats.tasks.compute_stats',
                'schedule_type': 'I',
                'minutes': 1,
            }
        )
    except ProgrammingError as e:
        # This catches specifically the "relation does not exist" error
        print(f"Django Q tables not yet created: {e}")