from django.core.management.base import BaseCommand
    
from core.management.commands import configure_logging
from core.solr_index import index_pages

configure_logging("index_pages_logging.config", "index_pages.log")

class Command(BaseCommand):
    help = """
    Rebuilds the page data in Solr, including the page OCR data.  It shouldn't
    be necessary most of the time, but it can be useful to run if Solr data
    becomes corrupt (though this is a very rare occurrence), or in cases the
    Solr index must be deleted, e.g., if you upgrade to a new major version of
    Solr.

    *If Solr corruption is suspected, you should run the `zap_index` command
    prior to reindexing.*

    This command can take a while to run, because every single page has OCR data
    which Solr has to index in order to facilitate full-text searching.  Plan for
    60 to 90 minutes per 100,000 pages in your collection.
    """

    def handle(self, **options):
        index_pages()
