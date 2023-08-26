import os
import logging

from optparse import make_option

from django.conf import settings
from django.db import connection
from django.core.management.base import BaseCommand, CommandError

from core.batch_loader import BatchLoader, BatchLoaderException
from core.management.commands import configure_logging
from core import solr_index

configure_logging('purge_batches_logging.config',
                  'purge_batch_%s.log' % os.getpid())

log = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Purge a batch"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('batch_name',
                            help='Batch name from "batches" command')

        # Options
        parser.add_argument(
            '--optimize', action='store_true', default=False, dest='optimize',
            help='Optimize Solr and MySQL after purge (VERY SLOW)')
        parser.add_argument('--interactive', action='store_true', default=True,
            dest='interactive',
            help='Whether command run interactively via terminal or via code')

    def handle(self, batch_name=None, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage is purge_batch %s' % self.args)

        loader = BatchLoader()
        try:
            log.info("purging batch '%s'", batch_name)
            loader.purge_batch(batch_name, options['interactive'])
            if options['optimize']:
                log.info("optimizing solr")
                solr = solr_index.conn()
                solr.optimize()
                log.info("optimizing MySQL OCR table")
                cursor = connection.cursor()
                cursor.execute("OPTIMIZE TABLE core_ocr")
                log.info("finished optimizing")
        except BatchLoaderException as e:
            if not options['interactive']:
                raise CommandError("Batch purge failed. %s. See %s/purge_batch_%s.log" % (
                    e, settings.LOG_LOCATION, os.getpid()
                ))
