import logging
import sys
import datetime
import time
import pdb
from core.models import Copyright
from core.models import LccnDateCopyright
from django.db import transaction
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def loadCopyrightMap(inputfilename):

    _logger = logging.getLogger(__name__)
    val = URLValidator()

    try:
        f = open(inputfilename, 'r')
    except IOError as e:
        _logger.exception(e)
        sys.exit(1)

    for line in f:
        arr = line.split("\t")
        if len(arr) == 4:
            try:
                val(arr[3].strip())
            except ValidationError as e:
                _logger.exception(e)
                sys.exit(1)
            try:
                sdate = datetime.datetime.strptime(arr[1], "%Y-%m-%d").date()
                edate = datetime.datetime.strptime(arr[2], "%Y-%m-%d").date()
            except ValueError as e:
                _logger.exception(e)
                sys.exit(1)

            record = LccnDateCopyright()
            record.lccn = arr[0]
            record.start_date = sdate
            record.end_date = edate

            try:
                result = Copyright.objects.filter(uri=arr[3].strip())
                record.copyright = result[0]
            except Exception as e:
                _logger.exception(e)
                sys.exit(1)

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
