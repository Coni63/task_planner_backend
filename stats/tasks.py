from django_q.tasks import schedule


def compute_stats():
    print("Computing stats...")



def setup_periodic_tasks():
    schedule('stats.tasks.compute_stats',
        schedule_type='I',
        minutes=1,
        name='compute_stats'
    )