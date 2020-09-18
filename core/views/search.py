import re
import json
from rfc3339 import rfc3339

from django.db.models import Q
from django.conf import settings
from django import urls
from django.core.paginator import InvalidPage
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.template import RequestContext
from django.utils import timezone

from core import models
from core import solr_index
from core import forms
from core.decorator import opensearch_clean, cache_page, cors
from core.utils.utils import _page_range_short, fulltext_range

def search_pages_paginator(request):
    # front page only
    try:
        sequence = int(request.GET.get('sequence', '0'))
    except ValueError as e:
        sequence = 0
    # set results per page value
    try:
        rows = int(request.GET.get('rows', '20'))
    except ValueError as e:
        rows = 20
    q = request.GET.copy()
    q['rows'] = rows
    q['sequence'] = sequence
    paginator = solr_index.SolrPaginator(q)
    return paginator


@cors
@cache_page(settings.DEFAULT_TTL_SECONDS)
@opensearch_clean
def search_pages_results(request, view_type='gallery'):
    page_title = "Search Results"
    paginator = search_pages_paginator(request)
    q = paginator.query
    try:
        page = paginator.page(paginator._cur_page)
    except InvalidPage:
        url = urls.reverse('openoni_search_pages_results')
        # Set the page to the first page
        q['page'] = 1
        return HttpResponseRedirect('%s?%s' % (url, q.urlencode()))
    start = page.start_index()
    end = page.end_index()

    # figure out the next page number
    query = request.GET.copy()
    if page.has_next():
        query['page'] = paginator._cur_page + 1
        next_url = '?' + query.urlencode()
        # and the previous page number
    if page.has_previous():
        query['page'] = paginator._cur_page - 1
        previous_url = '?' + query.urlencode()

    rows = query.get("rows", "20")
    sort = query.get("sort", default="relevance")
    seq_check = "checked" if query.get("sequence", "0") == "1" else ""

    crumbs = list(settings.BASE_CRUMBS)

    host = request.get_host()
    format = request.GET.get('format', None)
    if format == 'atom':
        feed_url = settings.BASE_URL + request.get_full_path()
        updated = rfc3339(timezone.now())
        return render(request, 'search/search_pages_results.xml', locals(),
                      content_type='application/atom+xml')
    elif format == 'json':
        results = {
            'startIndex': start,
            'endIndex': end,
            'totalItems': paginator.count,
            'itemsPerPage': rows,
            'items': [p.solr_doc for p in page.object_list],
        }
        for i in results['items']:
            i['url'] = settings.BASE_URL + i['id'].rstrip('/') + '.json'
        json_text = json.dumps(results, indent=2)
        # jsonp?
        if request.GET.get('callback') is not None:
            json_text = "%s(%s);" % (request.GET.get('callback'), json_text)
        return HttpResponse(json_text, content_type='application/json')
    page_range_short = list(_page_range_short(paginator, page))
    # copy the current request query without the page and sort
    # query params so we can construct links with it in the template
    q = request.GET.copy()
    for i in ('page', 'sort'):
        if i in q:
            q.pop(i)
    q = q.urlencode()

    # get an pseudo english version of the query
    english_search = paginator.englishify()

    form = forms.SearchResultsForm({"rows": rows, "sort": sort})
    if view_type == "list":
        template = "search/search_pages_results_list.html"
    else:
        template = "search/search_pages_results.html"
    page_list = []
    lccns = query.getlist("lccn")
    titles = []
    for lccn in lccns:
        name = str(models.Title.objects.get(lccn=lccn))
        titles.append({
            'abbrev': name[:24] +'...' if len(name) > 24 else name,
            'lccn': lccn,
            'name': name,
        })
    for count in range(len(page.object_list)):
        page_list.append((count + start, page.object_list[count]))

    start_year, end_year = fulltext_range()
    searching_all_dates = False
    if request.GET.get('date1') and request.GET.get('date2'):
        if request.GET.get('date1') == str(start_year) +'-01-01':
            if request.GET.get('date2') == str(end_year) +'-12-31':
                searching_all_dates = True

    return render(request, template, locals())

@cache_page(settings.DEFAULT_TTL_SECONDS)
def search_advanced(request):
    form = forms.SearchPagesForm()
    crumbs = list(settings.BASE_CRUMBS)
    template = "search/search_advanced.html"
    page_title = 'Advanced Search'
    return render(request, template, locals())


@cache_page(settings.DEFAULT_TTL_SECONDS)
def search_pages_opensearch(request):
    host = request.get_host()
    return render(request, 'search/search_pages_opensearch.xml', locals(),
                  content_type='application/opensearchdescription+xml')


@cors
@cache_page(settings.DEFAULT_TTL_SECONDS)
def suggest_titles(request):
    q = request.GET.get('q', '')
    q = q.lower()

    # remove initial articles (maybe there are more?)
    q = re.sub(r'^(the|a|an) ', '', q)

    # build up the suggestions
    # See http://www.opensearch.org/Specifications/OpenSearch/Extensions/Suggestions/1.0
    # for details on why the json is this way

    titles = []
    descriptions = []
    urls = []
    host = request.get_host()

    lccn_q = Q(lccn__startswith=q)
    title_q = Q(name_normal__startswith=q)
    for t in models.Title.objects.filter(lccn_q | title_q)[0:50]:
        titles.append(str(t))
        descriptions.append(t.lccn)
        urls.append(settings.BASE_URL + t.url)

    suggestions = [q, titles, descriptions, urls]
    json_text = json.dumps(suggestions, indent=2)
    # jsonp?
    if request.GET.get("callback") is not None:
        json_text = "%s(%s);" % (json.GET.get("callback"), json_text)
    return HttpResponse(json_text, content_type='application/x-suggestions+json')


@cache_page(settings.DEFAULT_TTL_SECONDS)
def search_pages_navigation(request):
    """Search results navigation data

    This view provides the information needed to add search result
    navigation to a page.

    """
    if not ('page' in request.GET and 'index' in request.GET):
        return HttpResponseNotFound()

    search_url = urls.reverse('openoni_search_pages_results')

    paginator = search_pages_paginator(request)

    search = {}
    search['total'] = paginator.count
    search['current'] = paginator.overall_index + 1  # current is 1-based
    search['results'] = search_url + '?' + paginator.query.urlencode()
    search['previous_result'] = paginator.previous_result
    search['next_result'] = paginator.next_result

    return HttpResponse(json.dumps(search), content_type="application/json")
