# __init__.py

from django.utils import datetime_safe

def strftime(d, fmt):
    """Backwards compatibility for others' themes, e.g.
    https://github.com/uoregon-libraries/oregon-oni/blob/795f3096b897e40c5e04b3b17d79fec214f62825/json_api.py
    """
    return strftime_safe(d, fmt)

def strftime_safe(d, fmt):
    """Works with datetimes with years less than 1900 for %Y
    Python 2.7's datetime.strftime does not handle these
    """
    return datetime_safe.new_datetime(d).strftime(fmt)

