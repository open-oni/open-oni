from django.conf import settings
from pathlib import Path

import logging
import logging.config

def configure_logging(config_file, log_file):
    if Path(config_file).exists():
        logging.config.fileConfig(config_file)
    else:
        logging.basicConfig()
        logging.getLogger().setLevel(logging.INFO)
        _file_handler = logging.FileHandler(Path(settings.LOG_LOCATION) / log_file, encoding = 'UTF-8')
        _formatter = logging.Formatter("""[%(asctime)s %(levelname)s %(name)s] %(message)s""")
        _file_handler.setFormatter(_formatter)
        logging.getLogger().addHandler(_file_handler)
