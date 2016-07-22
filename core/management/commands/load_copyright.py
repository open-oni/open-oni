import os
import logging
import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core.load_copyright import loadCopyright
from core.management.commands import configure_logging

configure_logging("load_copyright_logging.config", "load_coyright.log")

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load copyrights"
    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
       

        filepath = options['filepath']
        try:
            loadCopyright(filepath)
        except Exception as e:
            LOGGER.exception(e)
            raise CommandError("unable to load copyrights. check the load_batch log for clues")

