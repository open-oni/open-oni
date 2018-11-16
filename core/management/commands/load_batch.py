import os
import logging

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core.batch_loader import BatchLoader, BatchLoaderException
from core.management.commands import configure_logging
    
configure_logging('load_batch_logging.config', 
                  'load_batch_%s.log' % os.getpid())

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load a batch"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('batch_name')

        # Options
        parser.add_argument('--skip-coordinates', action='store_true',
                            default=False, dest='process_coordinates',
                            help='Do not write out word coordinates')
        parser.add_argument('--skip-process-ocr', action='store_true',
                            default=False, dest='process_ocr',
                            help='Do not generate ocr, and index')

    def handle(self, batch_name, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage is load_batch %s' % self.args)

        loader = BatchLoader(process_ocr=options['process_ocr'],
                             process_coordinates=options['process_coordinates'])
        try:
            batch = loader.load_batch(batch_name)
        except BatchLoaderException, e:
            LOGGER.exception(e)
            raise CommandError("unable to load batch. check the load_batch log for clues")
