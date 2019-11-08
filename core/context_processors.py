from django.conf import settings

from core.forms import CityForm
from core.utils.utils import fulltext_range


def extra_request_info(request):
    """
    Add some extra useful stuff into the RequestContext.
    """
    date_boundaries = fulltext_range()
    return {
        'BASE_URL': settings.BASE_URL,
        'city_form': CityForm(),
        'fulltext_enddate': date_boundaries[1],
        'fulltext_startdate': date_boundaries[0],
        'project_name': settings.PROJECT_NAME if "PROJECT_NAME" in dir(settings) else None,
        'site_title': settings.SITE_TITLE if "SITE_TITLE" in dir(settings) else None,
    }


def cors(request):
    """
    Add CORS headers so that the JSON can be used easily from JavaSript
    without requiring proxying.
    """
    pass
