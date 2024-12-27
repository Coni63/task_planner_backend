from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stats"
    
    def ready(self):
        from .tasks import setup_periodic_tasks
        setup_periodic_tasks()