import logging
import sys
from core.models import Copyright

def loadCopyright(inputfilename):

    _logger = logging.getLogger(__name__)

    try:
        f = open(inputfilename, 'r')

        for line in f:
            arr = line.split("\t")
            if len(arr) == 2:
              record = Copyright()
              record.uri = arr[0]
              record.label =arr[1].strip()
              record.save()
    except Exception as e:
        _logger.exception(e)

    f.close()

