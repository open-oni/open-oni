import logging
import os

from django.core.cache import cache
from django.core.management.base import BaseCommand, CommandError

from core.management.commands import configure_logging


configure_logging('delete_cache_logging.config',
                  'delete_cache_%s.log' % os.getpid())
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Delete newspaper info and title state cache"

    def handle(self, *args, **options):
        if len(args)!=0:
            raise CommandError('Usage is `manage.py delete_cache`')

        try:
            logger.info("Deleting titles_states cache...")
            cache.delete('titles_states')
        except Exception as e:
            logger.exception(e)
            raise CommandError("Unable to delete newspaper info and title state cache")
