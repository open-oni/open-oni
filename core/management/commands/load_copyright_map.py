import os
import logging
import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core.load_copyright_map import loadCopyrightMap
from core.management.commands import configure_logging

configure_logging("load_copyright_map_logging.config", "load_coyright_map.log")

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Load copyrights maps"
    def add_arguments(self, parser):
        parser.add_argument('filepath')

    def handle(self, *args, **options):
       

        filepath = options['filepath']
        try:
            loadCopyrightMap(filepath)
        except Exception as e:
            LOGGER.exception(e)
            raise CommandError("unable to load copyright maps. check the load_batch log for clues")

