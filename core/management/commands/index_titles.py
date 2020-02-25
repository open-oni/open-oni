import logging

from django.core.management.base import BaseCommand
    
from core.management.commands import configure_logging
from core.solr_index import index_titles

configure_logging("index_titles_logging.config", "index_titles.log")

_logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = """
    Reindexes all titles into Solr.  Titles tend to be very few in an ONI
    installation, and they contain very little data, so this operation is
    usually done in under a minute.
    """

    def handle(self, **options):
        _logger.info("indexing titles")
        index_titles()
        _logger.info("finished indexing titles")

