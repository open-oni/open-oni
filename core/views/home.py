import json
import datetime
import random

from django.conf import settings
from django.http import Http404, HttpResponse
from django.template import RequestContext
from django.template.loader import get_template
from django.core import urlresolvers

from core import models
from core import forms


def home(request, date=None):
    context = RequestContext(request, {})
    context["crumbs"] = list(settings.BASE_CRUMBS)
    today = datetime.date.today()
    context["date"] = date = today.replace(year=today.year-100)
    context["pages"] = _frontpages(request, date)
    page_nums = len(context["pages"])
    if page_nums > 0:
        context["page"] = context["pages"][random.randint(0,page_nums-1)]
        context["heading"] = "100 Years Ago Today"
    else:
        context["page"] = None
        context["heading"] = "Browse Newspaper Content"
    template = get_template("home.html")
    return HttpResponse(content=template.render(context))


def _frontpages(request, date, num_pages=20):
    # if there aren't any issues default to the first 20 which
    # is useful for testing the homepage when there are no issues
    # for a given date
    issues = models.Issue.objects.filter(date_issued=date)
    if issues.count() == 0:
        issues = models.Issue.objects.all()[0:num_pages]

    results = []
    for issue in issues:
        first_page = issue.first_page
        if not first_page or not first_page.jp2_filename:
            continue

        path_parts = dict(lccn=issue.title.lccn,
                          date=issue.date_issued,
                          edition=issue.edition,
                          sequence=first_page.sequence)
        url = urlresolvers.reverse('openoni_page', kwargs=path_parts)
        results.append({
            'label': "%s" % issue.title.display_name,
            'url': url,
            'place_of_publication': issue.title.place_of_publication,
            'pages': issue.pages.count(),
            'first_page': first_page
        })
    return results


def frontpages(request, date):
    _year, _month, _day = date.split("-")
    try:
        date = datetime.date(int(_year), int(_month), int(_day))
    except ValueError:
        raise Http404
    results = _frontpages(request, date)
    return HttpResponse(json.dumps(results), content_type="application/json")
