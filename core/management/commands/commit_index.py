from django.core.management.base import BaseCommand
from django.conf import settings

from core import solr_index

class Command(BaseCommand):
    help = "send a commit message to the solr index"

    def handle(self, **options):
        solr_index.conn().commit()
