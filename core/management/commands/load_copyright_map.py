import os
import logging
import datetime

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from core.load_copyright_map import loadCopyrightMap
from core.management.commands import configure_logging

configure_logging("load_copyright_map_logging.config", "load_copyright_map.log")

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = """
    Defines rules for which titles should use a given rights statement for certain
    date ranges.  Rights *must* first be loaded via the load_copyright command.

    Rules are composed of four-field tab-separated-values files, where each line
    indicates a single rule.  The fields, in order, are LCCN, start date, end date,
    and rights URI.  Start and end dates must be formatted as `YYYY-MM-DD`, e.g.,
    `2001-09-08` means September 8th, 2001.

    Please note that loading the same file multiple times will result in duplicated
    data, and manual SQL may be needed to clean dupes from `core_lccndatecopyright`.
    """

    def add_arguments(self, parser):
        parser.add_argument('filepath', help="Path to input file")

    def handle(self, filepath, *args, **options):

        try:
            loadCopyrightMap(filepath)
        except Exception as e:
            LOGGER.exception(e)
            raise CommandError("unable to load copyright maps. check the load_batch log for clues")

