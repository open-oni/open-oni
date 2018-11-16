import optparse

from django.core.management.base import BaseCommand
from django.conf import settings

from solr import SolrConnection


class Command(BaseCommand):
    def add_arguments(self, parser):
        # Options
        parser.add_argument(
            '--batch', action='store_true', default=False, dest='batch',
            help='remove all documents, or only documents related to a particular batch from the solr index')

    def handle(self, **options):
        solr = SolrConnection(settings.SOLR)
        if options['batch']:
            solr.delete_query('batch: %s' % options['batch'])
        else:
            solr.delete_query('id:[* TO *]')
        solr.commit()
