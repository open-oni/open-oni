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

    for line in f:
        arr = line.split("\t")
        if len(arr) == 2:
            try:
                val(arr[0])
            except ValidationError as e:
                _logger.exception(e)
                sys.exit(1)
            record = Copyright()
            record.uri = arr[0]
            record.label =arr[1].strip()
            try:
                with transaction.atomic():
                    record.save()

            except Exception as e:
                _logger.exception(e)
                sys.exit(1)

        elif line and line.strip():
            _logger.error("There is an error in the input: " + line)
            sys.exit(1)

    f.close()

