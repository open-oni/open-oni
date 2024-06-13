import os
import logging

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core.batch_loader import BatchLoader, BatchLoaderException
from core.management.commands import configure_logging
    
configure_logging('load_batch_logging.config', 
                  'load_batch_%s.log' % os.getpid())

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
    This command loads the metadata and pages associated with a batch into a
    database and search index. It may take up to several hours to complete,
    depending on the batch size and machine.
    """

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
        parser.add_argument('--interactive', action='store_true',
                            default=True, dest='interactive',
                            help='Whether command run interactively via terminal or via code')

    def handle(self, batch_path, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage: load_batch %s' % self.args)

        if not os.path.exists(batch_path):
            raise CommandError('Batch path does not exist: {}'.format(batch_path))

        loader = BatchLoader(process_ocr=options['process_ocr'],
                             process_coordinates=options['process_coordinates'])
        try:
            batch = loader.load_batch(batch_path, options['interactive'])
        except BatchLoaderException as e:
            if not options['interactive']:
                raise CommandError("Batch load failed. %s. See %s/load_batch_%s.log" % (
                    e, settings.LOG_LOCATION, os.getpid()
                ))
