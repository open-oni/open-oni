import logging
import os

from celery.decorators import task

from django.conf import settings
from django.core import management
from django.core.cache import cache

from openoni.core.models import Batch, OcrDump
from openoni.core.batch_loader import BatchLoader

logger = logging.getLogger(__name__)


@task
def process_coordinates(batch_dir):
    try:
        batch_loader = BatchLoader()
        batch_loader.process_coordinates(batch_dir)
        logger.info("processed batch %s", batch_dir)
    except Exception, e:
        logger.exception("unable to process batch %s" % batch_dir)

@task
def load_batch(batch_dir, process_coordinates=True):
    try:
        batch_loader = BatchLoader(process_coordinates=process_coordinates)
        batch = batch_loader.load_batch(batch_dir)
        logger.info("loaded batch %s", batch)

    except Exception, e:
        logger.exception("unable to load batch %s" % batch_dir)

@task
def purge_batch(batch):
    try:
        optimize = not settings.IS_PRODUCTION
        management.call_command('purge_batch', batch, optimize=optimize)
    except Exception, e:
        logger.exception("unable to purge batch: %s" % e)

@task
def delete_django_cache():
    logger.info("deleting newspaper_info")
    cache.delete('newspaper_info')

    logger.info("deleting titles_states")
    cache.delete('titles_states')

@task
def dump_ocr(batch_name):
    batch = Batch.objects.get(name=batch_name)
    try:
        if batch.ocr_dump:
            logger.info("ocr already generated for %s", batch)
        return
    except OcrDump.DoesNotExist:
        # as expected
        pass

    logger.info("starting to dump ocr for %s", batch)
    dump = OcrDump.new_from_batch(batch)
    logger.info("created ocr dump %s for %s", dump, batch)
