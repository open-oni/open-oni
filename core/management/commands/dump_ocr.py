import logging
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from core.management.commands import configure_logging

from core.models import Batch, OcrDump

configure_logging("dump_ocr_logging.config", "dump_ocr.log")
_logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "looks for batches that need to have ocr dump files created"

    def handle(self, *args, **options):
        if not os.path.isdir(settings.OCR_DUMP_STORAGE):
            os.makedirs(settings.OCR_DUMP_STORAGE)

        for batch in Batch.objects.filter(ocr_dump__isnull=True):
            _logger.info("starting to dump ocr for %s", batch)
            try:
                if batch.ocr_dump:
                    _logger.info("Ocr is already generated for %s", batch)
                    continue
            except OcrDump.DoesNotExist:
                pass

            dump = OcrDump.new_from_batch(batch)
            _logger.info("created ocr dump %s for %s", dump, batch)
