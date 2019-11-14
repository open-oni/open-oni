from django.core.management.base import BaseCommand

from core import models
    
class Command(BaseCommand):
    help = "Displays information about batches"

    def handle(self, *args, **options):

        for batch in models.Batch.objects.all().order_by('name'):
            print(batch.name)
