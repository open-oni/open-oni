import csv
import json
from rfc3339 import rfc3339

from django.conf import settings
from django.core.urlresolvers import reverse
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
    titles = titles.annotate(last_release=Max('issues__batch__released'))
    titles = titles.order_by('-last_release')

    # get the last update time for all the titles to use as the
    # updated time for the feed
    if titles.count() > 0:
        last_issue = titles[0].last_issue_released
        if last_issue.batch.released:
            feed_updated = last_issue.batch.released
        else:
            feed_updated = last_issue.batch.created
    else:
        feed_updated = timezone.now()

    host = request.get_host()
    return render(request, 'newspapers.xml', locals(),
                  content_type='application/atom+xml')


@cors
@cache_page(settings.DEFAULT_TTL_SECONDS)
@opensearch_clean
def search_titles_results(request):
    page_title = 'Title Search Results'
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([{'label': 'Advanced Search',
                    'href': reverse('openoni_search_titles')},
                   ])

    def prep_title_for_return(t):
        title = {}
        title.update(t.solr_doc)
        title['oclc'] = t.oclc
        return title

    format = request.GET.get('format', None)

    # check if requested format is CSV before building pages for response. CSV
    # response does not make use of pagination, instead all matching titles from
    # SOLR are returned at once
    if format == 'csv':
        query = request.GET.copy()
        q, fields, sort_field, sort_order, facets = solr_index.get_solr_request_params_from_query(query)

        # return all titles in csv format. * May hurt performance. Assumption is that this
        # request is not made often.
        # TODO: revisit if assumption is incorrect
        solr_response = solr_index.execute_solr_query(q, fields, sort_field,
                                                 sort_order, solr_index.title_count(), 0)
        titles = solr_index.get_titles_from_solr_documents(solr_response)

        csv_header_labels = ('lccn', 'title', 'place_of_publication', 'start_year',
                             'end_year', 'publisher', 'edition', 'frequency', 'subject',
                             'state', 'city', 'country', 'language', 'oclc',
                             'holding_type',)
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="openoni_titles.csv"'
        writer = csv.writer(response)
        writer.writerow(csv_header_labels)
        for title in titles:
            writer.writerow([smart_str(val or '--') for val in (title.lccn, title.name, title.place_of_publication,
                                title.start_year, title.end_year, title.publisher,
                                title.edition, title.frequency,
                                list(map(str, title.subjects.all())),
                                set([p.state for p in title.places.all()]),
                                [p.city for p in title.places.all()],
                                str(title.country), list(map(str, title.languages.all())),
                                title.oclc, title.holding_types)])
        return response

    try:
        curr_page = int(request.GET.get('page', 1))
    except ValueError as e:
        curr_page = 1

    paginator = solr_index.SolrTitlesPaginator(request.GET)

    try:
        page = paginator.page(curr_page)
    except:
        raise Http404

    page_range_short = list(_page_range_short(paginator, page))

    try:
        rows = int(request.GET.get('rows', '20'))
    except ValueError as e:
        rows = 20

    query = request.GET.copy()
    query.rows = rows
    if page.has_next():
        query['page'] = curr_page + 1
        next_url = '?' + query.urlencode()
    if page.has_previous():
        query['page'] = curr_page - 1
        previous_url = '?' + query.urlencode()
    start = page.start_index()
    end = page.end_index()
    host = request.get_host()
    page_list = []
    for p in range(len(page.object_list)):
        page_start = start+p
        page_list.append((page_start, page.object_list[p]))

    if format == 'atom':
        feed_url = settings.BASE_URL + request.get_full_path()
        updated = rfc3339(timezone.now())
        return render(request, 'search/search_titles_results.xml', locals(),
                      content_type='application/atom+xml')

    elif format == 'json':
        results = {
            'startIndex': start,
            'endIndex': end,
            'totalItems': paginator.count,
            'itemsPerPage': rows,
            'items': [prep_title_for_return(t) for t in page.object_list]
        }
        # add url for the json view
        for i in results['items']:
            i['url'] = settings.BASE_URL + i['id'].rstrip("/") + ".json"
        json_text = json.dumps(results, indent=2)
        # jsonp?
        if request.GET.get('callback') is not None:
            json_text = "%s(%s);" % (request.GET.get('callback'), json_text)
        return HttpResponse(json_text, content_type='application/json')


    sort = request.GET.get('sort', 'relevance')

    q = request.GET.copy()
    if 'page' in q:
        del q['page']
    if 'sort' in q:
        del q['sort']
    q = q.urlencode()
    collapse_search_tab = True

    form = forms.SearchResultsForm({"rows": rows, "sort": sort})
    return render(request, 'search/search_titles_results.html', locals())


@cache_page(settings.DEFAULT_TTL_SECONDS)
@rdf_view
def newspapers_rdf(request):
    titles = models.Title.objects.filter(has_issues=True)
    graph = titles_to_graph(titles)
    return HttpResponse(graph.serialize(base=_rdf_base(request),
                                        include_base=True),
                        content_type='application/rdf+xml')
