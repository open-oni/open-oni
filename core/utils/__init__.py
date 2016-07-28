# __init__.py

import datetime
from django.utils import datetime_safe

def strftime(d, fmt):
    """works with datetimes with years less than 1900
    """
    return datetime_safe.new_datetime(d).strftime(fmt)

