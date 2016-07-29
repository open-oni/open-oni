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
    help = "Add copyright uris and labels to the Copyright table from input file."
    def add_arguments(self, parser):
        parser.add_argument('filepath', help="Path to input file")

    def handle(self, *args, **options):

        filepath = options['filepath']
        try:
            loadCopyright(filepath)
        except Exception as e:
            LOGGER.exception(e)
            raise CommandError("unable to load copyrights. check the load_batch log for clues")

