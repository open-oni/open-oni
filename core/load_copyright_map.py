import logging
import sys
import datetime
from core.models import Copyright
from core.models import LccnDateCopyright

def check_uri(_uri):
    try:
        result = Copyright.objects.filter(uri=_uri)
        return result.exists()
    except Exception as e:
        _logger.exception(e)

def loadCopyrightMap(inputfilename):

    _logger = logging.getLogger(__name__)
    try:
        f = open(inputfilename, 'r')
        for line in f:
            arr = line.split("\t")
            if len(arr) == 4:
                if check_uri(arr[3].strip()):
                    record = LccnDateCopyright()
                    record.lccn = arr[0]
                    record.start_date = (arr[1])
                    record.end_date = (arr[2])
                    result = Copyright.objects.filter(uri=arr[3].strip())
                    record.uri = result[0]
                    record.save()

    except Exception as e:
       _logger.exception(e)

    f.close()
