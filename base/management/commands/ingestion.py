from django.core.management.base import BaseCommand
from base.tasks import ingest_data

class Command(BaseCommand):
    help = 'Run data ingestion for customers and loans'

    def handle(self, *args, **kwargs):
        ingest_data.delay()
        self.stdout.write(self.style.SUCCESS('Ingestion task started!'))
