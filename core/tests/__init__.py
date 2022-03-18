from django.conf import settings
from pathlib import Path

import logging

logging.basicConfig(filename=Path(settings.LOG_LOCATION) / "test.log", level=logging.DEBUG)
