from django.core.management.base import BaseCommand

from optimization.services import optimize

class Command(BaseCommand):
    help = "Single run of the optimization algorithm"

    def handle(self, *args, **kwargs):
        optimize({})
