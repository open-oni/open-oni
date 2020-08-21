import optparse

from django.core.management.base import BaseCommand
from django.conf import settings

from core import solr_index

class Command(BaseCommand):
    help = """
    Deletes the Solr index in its entirety.  USE WITH CAUTION.
    After running this, your ONI installation WILL NOT FUNCTION without
    reindexing (e.g., `./manage.py index`)
    """

    def handle(self, **options):
        solr = solr_index.conn()
        solr.delete(q='*:*')
        solr.commit()
