import logging
from django.conf import settings

logging.basicConfig(filename=settings.LOG_LOCATION + "test.log", level=logging.DEBUG)
