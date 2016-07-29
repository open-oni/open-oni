import logging
import sys
from core.models import Copyright
from django.db import transaction
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

def loadCopyright(inputfilename):

    _logger = logging.getLogger(__name__)
    val = URLValidator()

    try:
        f = open(inputfilename, 'r')
    except IOError as e:
        _logger.exception(e)
        sys.exit(1)
    try:
        with transaction.atomic():
            for line in f:
                arr = line.split("\t")
                if len(arr) == 2:
                    val(arr[0])

                    record = Copyright()
                    record.uri = arr[0]
                    record.label =arr[1].strip()
                    record.save()
                elif line and line.strip():
                    raise ValueError ("Bad line.")

    except Exception as e:
        _logger.exception(e)
        sys.exit(1)

    f.close()

