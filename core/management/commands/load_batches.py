import os
import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core import batch_loader
from core.management.commands import configure_logging
    
configure_logging('load_batches_logging.config', 
                  'load_batches_%s.log' % os.getpid())

_logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load batches by name from a batch list file"

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('batch_list_filename')

        # Options
        parser.add_argument('--skip-coordinates', action='store_true',
                            default=True, dest='process_coordinates',
                            help='Do not write out word coordinates')
        parser.add_argument('--skip-process-ocr', action='store_true',
                            default=True, dest='process_ocr',
                            help='Do not generate ocr, and index')

    def handle(self, batch_list_filename, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage is load_batch %s' % self.args)

        loader = batch_loader.BatchLoader(
            process_ocr=options['process_ocr'],
            process_coordinates=options['process_coordinates'])
        batch_list = open(batch_list_filename)
        _logger.info("batch_list_filename: %s" % batch_list_filename)
        for line in batch_list:
            batch_name = line.strip()
            _logger.info("batch_name: %s" % batch_name)
            parts = batch_name.split("_")
            if len(parts)==4 and parts[0]=="batch":
                loader.load_batch(batch_name, strict=False)
            else:
                _logger.warning("invalid batch name '%s'" % batch_name)

