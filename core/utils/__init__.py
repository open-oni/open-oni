# __init__.py

import datetime
from django.utils import datetime_safe

def strftime(d, fmt):
    """works with datetimes with years less than 1900
    """
    return datetime_safe.new_datetime(d).strftime(fmt)

def strdate_to_ordinal(date):
    date_arr = date.split('-')
    date_obj = datetime.date(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
    return date_obj.toordinal()

