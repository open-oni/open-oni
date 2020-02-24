import os
import logging
import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core.load_copyright import loadCopyright
from core.management.commands import configure_logging

configure_logging("load_copyright_logging.config", "load_copyright.log")

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
    Adds copyright URIs and labels for displaying on titles that aren't public
    domain.  This must be used with load_copyright_map.  Rights statements
    files must be tab-separated files where each line contains a single
    copyright statement's data in the format of URI followed by a [TAB]
    followed by a label.  Please note that loading the same file multiple times
    will result in duplicated data, and a manual SQL command may be needed to
    clean dupes from the `core_copyright` table.
    """

    def add_arguments(self, parser):
        parser.add_argument('filepath', help="Path to input file")

    def handle(self, filepath, *args, **options):

        try:
            loadCopyright(filepath)
        except Exception as e:
            LOGGER.exception(e)
            raise CommandError("unable to load copyrights. check the load_batch log for clues")

