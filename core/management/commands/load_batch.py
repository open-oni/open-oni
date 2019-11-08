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
        parser.add_argument('batch_path', help='Path to batch files')

        # Options
        parser.add_argument('--skip-coordinates', action='store_true',
                            default=True, dest='process_coordinates',
                            help='Do not write out word coordinates')
        parser.add_argument('--skip-process-ocr', action='store_true',
                            default=True, dest='process_ocr',
                            help='Do not generate ocr, and index')

    def handle(self, batch_path, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage: load_batch %s' % self.args)

        if not os.path.exists(batch_path):
            raise CommandError('Batch path does not exist: {}'.format(batch_path))

        loader = BatchLoader(process_ocr=options['process_ocr'],
                             process_coordinates=options['process_coordinates'])
        try:
            batch = loader.load_batch(batch_path)
        except BatchLoaderException, e:
            LOGGER.exception(e)
            raise CommandError("Batch load failed. See logs/load_batch_#.log")
