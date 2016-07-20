import logging
import os.path
import urlparse
import urllib2
import json
import gzip
import re

from cStringIO import StringIO

from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponseServerError

from core import models
from core.utils.utils import get_page
from core.decorator import cors

LOGGER = logging.getLogger(__name__)

@cors
def coordinates(request, lccn, date, edition, sequence, words=None):
    url_parts = dict(lccn=lccn, date=date, edition=edition, sequence=sequence)
    try:
        file_data = gzip.open(models.coordinates_path(url_parts), 'rb')
    except IOError:
        return HttpResponse()

    data = json.load(file_data)

    non_lexemes = re.compile('''^[^a-zA-Z0-9]+|[^a-zA-Z0-9]+$|'s$''')
    return_coords = data.copy()
    # reset coords to {} and build afresh, getting rid of unwanted punctuations
    return_coords['coords'] = {}
    for key in data.get('coords'):
        return_coords['coords'][re.sub(non_lexemes, '', key)] = data['coords'][key]

    r = HttpResponse(content_type='application/json')
    r.write(json.dumps(return_coords))
    return r
