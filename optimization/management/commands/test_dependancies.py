from django.core.management.base import BaseCommand

from optimization.services import check_dependencies

class Command(BaseCommand):
    help = "Single run of the optimization algorithm"

    def handle(self, *args, **kwargs):
        check_dependencies({
            "project": "2912078b7bf742a8868f3e6d0d32a8ef",
            "base_task": "0f959d87f7eb47619d905cab00dd96cb"
        })
