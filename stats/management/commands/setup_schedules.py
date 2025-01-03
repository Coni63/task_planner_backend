from django.core.management.base import BaseCommand
from django.db import ProgrammingError
from django_q.models import Schedule

class Command(BaseCommand):
    help = 'Setup periodic tasks for stats computation'

    def handle(self, *args, **kwargs):
        try:
            schedule, created = Schedule.objects.update_or_create(
                name='compute_stats',
                defaults={
                    'func': 'stats.tasks.compute_stats',
                    'schedule_type': 'I',
                    'minutes': 1,
                }
            )
            status = 'Created' if created else 'Updated'
            self.stdout.write(self.style.SUCCESS(f'{status} compute_stats schedule'))
        except ProgrammingError as e:
            self.stdout.write(self.style.ERROR(f"Django Q tables not yet created: {e}"))