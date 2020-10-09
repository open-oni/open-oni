import csv
import json
from rfc3339 import rfc3339

from django.conf import settings
from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseServerError
from django.db.models import Max, Min, Q
from django.shortcuts import render
from django.template import RequestContext
from django.utils import timezone
from django.utils.encoding import smart_str

from core.decorator import cache_page, opensearch_clean, rdf_view, cors
from core import forms
from core.utils.utils import _page_range_short, _rdf_base
from core import models
from core import solr_index
from core.rdf import titles_to_graph
from core.utils.url import unpack_url_path

@cors
@cache_page(settings.DEFAULT_TTL_SECONDS)
def newspapers(request, city=None, format='html'):
    page_title = 'All Titles'
    page_count = models.Page.objects.count()
    titles = models.Title.objects.filter(has_issues=True)
    titles = titles.annotate(first=Min('issues__date_issued'))
    titles = titles.annotate(last=Max('issues__date_issued'))

    sorted_titles = sorted(titles, key=lambda title: title.name_normal)
    crumbs = list(settings.BASE_CRUMBS)

    if format == "html":
        return render(request, 'newspapers.html', locals())
    elif format == "json":
        host = request.get_host()

        results = {
            "@context": "http://iiif.io/api/presentation/2/context.json",
            "@id": settings.BASE_URL + request.get_full_path(),
            "@type": "sc:Collection",
            "label": "Newspapers",
            "collections": [],
        }

        for title in sorted_titles:
            results["collections"].append({
                "@id": settings.BASE_URL + title.json_url,
                "@type": "sc:Collection",
                "label": title.display_name
            })

        return HttpResponse(json.dumps(results, indent=2), content_type='application/json')
    else:
        return HttpResponseServerError("unsupported format: %s" % format)


@cache_page(settings.API_TTL_SECONDS)
def newspapers_atom(request):
    # get a list of titles with issues that are in order by when they
    # were last updated
    titles = models.Title.objects.filter(has_issues=True)
    titles = titles.annotate(last_create=Max('issues__batch__created'))
    titles = titles.order_by('-last_create')

    # get the last update time for all the titles to use as the
    # updated time for the feed
    if titles.count() > 0:
        last_issue = titles[0].last_issue_created
        if last_issue.batch.created:
            feed_updated = last_issue.batch.created
        else:
            feed_updated = last_issue.batch.created
    else:
        feed_updated = timezone.now()

    host = request.get_host()
    return render(request, 'newspapers.xml', locals(),
                  content_type='application/atom+xml')

@cache_page(settings.DEFAULT_TTL_SECONDS)
@rdf_view
def newspapers_rdf(request):
    titles = models.Title.objects.filter(has_issues=True)
    graph = titles_to_graph(titles)
    return HttpResponse(graph.serialize(base=_rdf_base(request),
                                        include_base=True),
                        content_type='application/rdf+xml')
