import os
import logging
from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core import models
from core.management.commands import configure_logging
    
configure_logging('diff_batches_logging.config', 
                  'diff_batches_%s.log' % os.getpid())

_logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
    Given a file with batch names, shows a list of batches and an indicator of
    their status relative to the current system's batch list.  If a batch is in the
    system but not in the file, it is prefixed with a plus `+`.  If a batch is in
    the system and the file, it is prefixed with a space ` `.  If a batch is not in
    the system but is listed in the file, it is prefixed with a minus `-`.
    """

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('batch_list_filename')

    def handle(self, batch_list_filename, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage is diff_batch %s' % self.args)

        batches = set()
        batch_list = open(batch_list_filename)
        _logger.info("batch_list_filename: %s" % batch_list_filename)
        for line in batch_list:
            batch_name = line.strip()
            _logger.info("batch_name: %s" % batch_name)
            parts = batch_name.split("_")
            if len(parts)==4 and parts[0]=="batch":
                batches.add(batch_name)
            else:
                _logger.warning("invalid batch name '%s'" % batch_name)


        current_batches = set()
        for batch in models.Batch.objects.all().order_by('name'):
            current_batches.add(batch.name)

        all_batches = batches.union(current_batches)
        for batch in sorted(all_batches):
            if batch in batches:
                if batch in current_batches:
                    indicator = " "  # both
                else:
                    indicator = "-"
            else:
                assert batch in current_batches
                indicator = "+"

            print("%s%s" % (indicator, batch))
