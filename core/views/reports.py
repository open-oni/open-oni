import csv
from rfc3339 import rfc3339
import json

from django.conf import settings
from django import urls
from django.db.models import Min, Max, Count
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage
from django.db import connection
from django.utils import timezone

from core import models
from core import solr_index
from core.rdf import batch_to_graph, awardee_to_graph
from core.utils.url import unpack_url_path
from core.decorator import cache_page, rdf_view, cors
from core.utils.utils import _page_range_short, _rdf_base, _get_tip


@cache_page(settings.API_TTL_SECONDS)
def reports(request):
    page_title = 'Reports'
    return render(request, 'reports/reports.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def batches(request, page_number=1):
    page_title = 'Batches'
    batches = models.Batch.viewable_batches().order_by('-created')
    paginator = Paginator(batches, 25)
    page = paginator.page(page_number)
    page_range_short = list(_page_range_short(paginator, page))

    # set page number variables
    if page.has_previous():
        previous_page_number = int(page_number) - 1
    if page.has_next():
        next_page_number = int(page_number) + 1

    return render(request, 'reports/batches.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def batches_atom(request, page_number=1):
    batches = models.Batch.viewable_batches()
    batches = batches.order_by('-created')
    now = rfc3339(timezone.now())

    paginator = Paginator(batches, 25)
    page = paginator.page(page_number)
    return render(request, 'reports/batches.xml', locals(),
                  content_type='application/atom+xml')


@cors
@cache_page(settings.API_TTL_SECONDS)
def batches_json(request):
    host = request.get_host()
    j = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": settings.BASE_URL + request.get_full_path(),
        "@type": "sc:Collection",
        "label": "Batches",
        "collections": []
    }
    for batch in models.Batch.objects.all():
        j['collections'].append(batch.json(serialize=False, include_issues=False, host=host))
    return HttpResponse(json.dumps(j, indent=2), content_type='application/json')


@cache_page(settings.API_TTL_SECONDS)
def batches_csv(request):
    csv_header_labels = ('Created', 'Name', 'Awardee', 'Total Pages')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="openoni_batches.csv"'
    writer = csv.writer(response)
    writer.writerow(csv_header_labels)
    for batch in models.Batch.viewable_batches():
        writer.writerow((batch.created, batch.name, batch.awardee.name, batch.page_count))
    return response

@cache_page(settings.API_TTL_SECONDS)
def batch(request, batch_name):
    batch = get_object_or_404(models.Batch, name=batch_name)

    awardee = batch.awardee

    issues = []
    for issue in batch.issues.all().select_related("title"):
        page_count = 0 if not issue.pages else issue.pages.count
        issues.append({'lccn': issue.title.lccn,
                       'title': issue.title.name,
                       'date_issued': issue.date_issued,
                       'page_count': page_count,
                       'edition': issue.edition})

    reels = []
    for reel in batch.reels.all():
        page_count = 0 if not reel.pages else reel.pages.count
        reels.append({'number': reel.number,
                      'titles': reel.titles(),
                      'title_range': _title_range(reel),
                      'page_count': reel.pages.count })
    page_title = 'Batch: %s' % batch.name

    return render(request, 'reports/batch.html', locals())


@cache_page(settings.API_TTL_SECONDS)
@rdf_view
def batch_rdf(request, batch_name):
    batch = get_object_or_404(models.Batch, name=batch_name)
    graph = batch_to_graph(batch)
    response = HttpResponse(graph.serialize(base=_rdf_base(request),
                                            include_base=True),
                            content_type='application/rdf+xml')
    return response


@cors
@cache_page(settings.API_TTL_SECONDS)
def batch_json(request, batch_name):
    batch = get_object_or_404(models.Batch, name=batch_name)
    host = request.get_host()
    return HttpResponse(batch.json(host=host), content_type='application/json')


@cors
@cache_page(settings.API_TTL_SECONDS)
def title_json(request, lccn):
    title = get_object_or_404(models.Title, lccn=lccn)
    host = request.get_host()
    return HttpResponse(title.json(host=host), content_type='application/json')


@cors
@cache_page(settings.API_TTL_SECONDS)
def issue_pages_json(request, lccn, date, edition):
    title, issue, page = _get_tip(lccn, date, edition)
    host = request.get_host()
    if issue:
        return HttpResponse(issue.json(host=host), content_type='application/json')
    else:
        return HttpResponseNotFound()


@cors
@cache_page(settings.API_TTL_SECONDS)
def page_json(request, lccn, date, edition, sequence):
    title, issue, page = _get_tip(lccn, date, edition, sequence)
    host = request.get_host()
    if page:
        return HttpResponse(page.json(host=host), content_type='application/json')
    else:
        return HttpResponseNotFound()


@cache_page(settings.API_TTL_SECONDS)
def event(request, event_id):
    page_title = 'Event'
    event = get_object_or_404(models.LoadBatchEvent, id=event_id)
    return render(request, 'reports/event.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def events(request, page_number=1):
    page_title = 'Events'
    events = models.LoadBatchEvent.objects.all().order_by('-created')
    paginator = Paginator(events, 25)
    page = paginator.page(page_number)
    page_range_short = list(_page_range_short(paginator, page))

    return render(request, 'reports/events.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def events_csv(request):
    csv_header_labels = ('Time', 'Batch name', 'Message',) 
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="openoni_events.csv"'
    writer = csv.writer(response)
    writer.writerow(csv_header_labels)
    for event in models.LoadBatchEvent.objects.all().order_by('-created'):
        writer.writerow((event.created, event.batch_name, event.message,))
    return response


@cache_page(settings.API_TTL_SECONDS)
def events_atom(request, page_number=1):
    events = models.LoadBatchEvent.objects.all().order_by('-created')
    paginator = Paginator(events, 25)
    page = paginator.page(page_number)
    page_range_short = list(_page_range_short(paginator, page))
    return render(request, 'reports/events.xml', locals(),
                  content_type='application/atom+xml')


@cache_page(settings.DEFAULT_TTL_SECONDS)
def states(request, format='html'):
    page_title = 'States'
    # custom SQL to eliminate spelling errors and the like in cataloging data
    # TODO: maybe use Django ORM once the data is cleaned more on import
    cursor = connection.cursor()
    non_states = ("----------------", "American Samoa",
                  "Mariana Islands", "Puerto Rico", "Virgin Islands")
    sql = ('SELECT state, COUNT(*) AS count FROM core_place',
           'WHERE state IS NOT NULL',
           'AND state NOT IN %s' % (non_states,),
           'GROUP BY state HAVING count > 10',
           'ORDER BY state')
    cursor.execute(' '.join(sql))
    if format == 'json' or request.META['HTTP_ACCEPT'] == 'application/json':
        states = [n[0] for n in cursor.fetchall()]
        states.extend(non_states)
        return HttpResponse(json.dumps(states),
                            content_type='application/json')
    states = [n[0] for n in cursor.fetchall()]
    return render(request, 'reports/states.html', locals())


@cache_page(settings.DEFAULT_TTL_SECONDS)
def counties_in_state(request, state, format='html'):
    state = unpack_url_path(state)
    if state is None:
        raise Http404
    page_title = 'Counties in %s' % state

    places = models.Place.objects.filter(state__iexact=state,
                                         county__isnull=False).all()
    county_names = sorted(set(p.county for p in places))

    if format == 'json':
        return HttpResponse(json.dumps(county_names),
                            content_type='application/json')
    counties = [name for name in county_names]
    if len(counties) == 0:
        raise Http404
    return render(request, 'reports/counties.html', locals())


@cache_page(settings.DEFAULT_TTL_SECONDS)
def states_counties(request, format='html'):
    page_title = 'Counties by State'

    cursor = connection.cursor()

    cursor.execute("\
SELECT state, county, COUNT(*) AS total FROM core_place \
WHERE state IS NOT NULL AND county IS NOT NULL \
GROUP BY state, county HAVING total >= 1 ORDER BY state, county")

    states_counties = [(n[0], n[1], n[2]) for n in cursor.fetchall()]

    return render(request, 'reports/states_counties.html', locals())


@cache_page(settings.DEFAULT_TTL_SECONDS)
def cities_in_county(request, state, county, format='html'):
    state, county = list(map(unpack_url_path, (state, county)))
    if state is None or county is None:
        raise Http404
    page_title = 'Cities in %s, %s' % (state, county)
    places = models.Place.objects.filter(state__iexact=state,
                                         county__iexact=county).all()
    cities = [p.city for p in places]
    if None in cities:
        cities.remove(None)
    if len(cities) == 0:
        raise Http404
    if format == 'json':
        return HttpResponse(json.dumps(cities),
                            content_type='application/json')
    return render(request, 'reports/cities.html', locals())


@cache_page(settings.DEFAULT_TTL_SECONDS)
def cities_in_state(request, state, format='html'):
    state = unpack_url_path(state)
    if state is None:
        raise Http404
    page_title = 'Cities in %s' % state

    places = models.Place.objects.filter(state__iexact=state,
                                         city__isnull=False).all()
    cities = sorted(set(p.city for p in places))

    if len(cities) == 0:
        raise Http404
    if format == 'json':
        return HttpResponse(json.dumps(cities),
                            content_type='application/json')
    return render(request, 'reports/cities.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def institutions(request, page_number=1):
    page_title = 'Institutions'
    institutions = models.Institution.objects.all()
    paginator = Paginator(institutions, 50)
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    page_range_short = list(_page_range_short(paginator, page))
    return render(request, 'reports/institutions.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def institution(request, code):
    institution = get_object_or_404(models.Institution, code=code)
    page_title = institution
    titles_count = models.Title.objects.filter(
        holdings__institution=institution).distinct().count()
    holdings_count = models.Holding.objects.filter(
        institution=institution).count()
    return render(request, 'reports/institution.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def institution_titles(request, code, page_number=1):
    institution = get_object_or_404(models.Institution, code=code)
    page_title = 'Titles held by %s' % institution
    titles = models.Title.objects.filter(
        holdings__institution=institution).distinct()
    paginator = Paginator(titles, 50)
    try:
        page = paginator.page(page_number)
    except InvalidPage:
        page = paginator.page(1)
    page_range_short = list(_page_range_short(paginator, page))
    return render(request, 'reports/institution_titles.html', locals())


@cache_page(10)
def status(request):
    page_title = 'System Status'
    page_count = models.Page.objects.all().count()
    issue_count = models.Issue.objects.all().count()
    batch_count = models.Batch.objects.all().count()
    title_count = models.Title.objects.all().count()
    holding_count = models.Holding.objects.all().count()
    essay_count = models.Essay.objects.all().count()
    pages_indexed = solr_index.page_count()
    titles_indexed = solr_index.title_count()
    return render(request, 'reports/status.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def awardees(request):
    page_title = 'Awardees'
    awardees = models.Awardee.objects.all().order_by('name')
    return render(request, 'reports/awardees.html', locals())


@cors
@cache_page(settings.API_TTL_SECONDS)
def awardees_json(request):
    host = request.get_host()
    awardees = {
        "@context": "http://iiif.io/api/presentation/2/context.json",
        "@id": settings.BASE_URL + request.get_full_path(),
        "@type": "sc:Collection",
        "label": "Awardees",
        "collections": []
    }
    for awardee in models.Awardee.objects.all().order_by('name'):
        awardees["collections"].append(awardee.json(host, include_batches=False, serialize=False))

    return HttpResponse(json.dumps(awardees, indent=2),
                        content_type='application/json')


@cache_page(settings.API_TTL_SECONDS)
def awardee(request, institution_code):
    awardee = get_object_or_404(models.Awardee, org_code=institution_code)
    page_title = 'Awardee: %s' % awardee.name
    batches = models.Batch.objects.filter(awardee=awardee)
    return render(request, 'reports/awardee.html', locals())


@cors
@cache_page(settings.API_TTL_SECONDS)
def awardee_json(request, institution_code):
    awardee = get_object_or_404(models.Awardee, org_code=institution_code)
    host = request.get_host()
    j = awardee.json(serialize=False, include_batches=True, host=host)
    return HttpResponse(json.dumps(j, indent=2), content_type='application/json')


@cache_page(settings.API_TTL_SECONDS)
@rdf_view
def awardee_rdf(request, institution_code):
    awardee = get_object_or_404(models.Awardee, org_code=institution_code)
    graph = awardee_to_graph(awardee)
    response = HttpResponse(graph.serialize(base=_rdf_base(request),
                                            include_base=True),
                            content_type='application/rdf+xml')
    return response


@cache_page(settings.DEFAULT_TTL_SECONDS)
def terms(request):
    return render(request, 'reports/terms.html', locals())


@cache_page(settings.DEFAULT_TTL_SECONDS)
def batch_summary(request, format='html'):
    page_title = "Batch Summary"
    cursor = connection.cursor()
    sql = """
          select cb.name, ci.title_id, min(date_issued),
          max(date_issued), count(cp.id)
          from core_batch cb, core_issue ci, core_page cp
          where cb.name=ci.batch_id and ci.id=cp.issue_id
          group by cb.name, ci.title_id order by cb.name;
          """

    cursor = connection.cursor()
    cursor.execute(sql)
    batch_details = cursor.fetchall()
    if format == 'txt':
        return render(request, 'reports/batch_summary.txt', locals(),
                      content_type='text/plain')
    return render(request, 'reports/batch_summary.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def reels(request, page_number=1):
    page_title = 'Reels'
    reels = models.Reel.objects.all().order_by('number')
    paginator = Paginator(reels, 25)
    page = paginator.page(page_number)
    page_range_short = list(_page_range_short(paginator, page))

    return render(request, 'reports/reels.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def reel(request, reel_number):
    crumbs = list(settings.BASE_CRUMBS)
    crumbs.extend([
        {'label': 'Reels',
         'href': urls.reverse('openoni_reels')},
    ])
    page_title = 'Reel %s' % reel_number
    m_reels = models.Reel.objects.filter(number=reel_number)
    reels = []
    for reel in m_reels:
        reels.append({'batch': reel.batch,
                      'titles': reel.titles(),
                      'title_range': _title_range(reel), })
    return render(request, 'reports/reel.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def essays(request):
    page_title = "Newspaper Essays"
    essays = models.Essay.objects.all().order_by('title')
    return render(request, 'reports/essays.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def essay(request, essay_id):
    essay = get_object_or_404(models.Essay, id=essay_id)
    title = essay.first_title()
    page_title = essay.title
    return render(request, 'reports/essay.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def ocr(request):
    page_title = "OCR Data"
    dumps = models.OcrDump.objects.all().order_by('-created')
    return render(request, 'reports/ocr.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def ocr_atom(request):
    dumps = models.OcrDump.objects.all().order_by("-created")
    if dumps.count() > 0:
        last_updated = dumps[0].created
    else:
        last_updated = timezone.now()
    return render(request, 'reports/ocr.xml', locals(),
                  content_type='application/atom+xml')


@cors
@cache_page(settings.API_TTL_SECONDS)
def ocr_json(request):
    j = {"ocr": []}
    host = request.get_host()
    for dump in models.OcrDump.objects.all().order_by("-created"):
        j["ocr"].append(dump.json(host=host, serialize=False))
    return HttpResponse(json.dumps(j, indent=2), content_type="application/json")


@cache_page(settings.API_TTL_SECONDS)
def languages(request):
    page_title = 'Languages'
    languages = models.LanguageText.objects.values('language__code', 'language__name').annotate(
        count=Count('language'))

    return render(request, 'reports/languages.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def language_batches(request, language, page_number=1):
    language_name = models.Language.objects.get(code=language).name
    page_title = 'Batches with %s text' % (language_name)
    if language != "eng":
        batches = models.Batch.objects.filter(
            issues__pages__ocr__language_texts__language__code=language
            ).values('name').annotate(count=Count('name'))
        paginator = Paginator(batches, 25)
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page = paginator.page(1)
        page_range_short = list(_page_range_short(paginator, page))
    return render(request, 'reports/language_batches.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def language_titles(request, language, page_number=1):
    language_name = models.Language.objects.get(code=language).name
    page_title = 'Titles with %s text' % (language_name)
    if language != "eng":
        titles = models.Title.objects.filter(
            issues__pages__ocr__language_texts__language__code=language
            ).values('lccn', 'issues__batch__name').annotate(count=Count('lccn'))
        paginator = Paginator(titles, 25)
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page = paginator.page(1)
        page_range_short = list(_page_range_short(paginator, page))
    return render(request, 'reports/language_titles.html', locals())


@cache_page(settings.API_TTL_SECONDS)
def language_pages(request, language, batch, title=None, page_number=1):
    language_name = models.Language.objects.get(code=language).name
    page_title = 'Pages with %s text' % (language_name)
    path = 'reports/language_title_pages.html'
    if language != 'eng':
        if title:
            pages = models.Page.objects.filter(
                ocr__language_texts__language__code=language,
                issue__title__lccn=title
                ).values(
                    'reel__number', 'issue__date_issued', 'issue__title__lccn',
                    'issue__edition', 'sequence',
                ).order_by(
                    'reel__number', 'issue__date_issued',
                    'sequence'
            )
        else:
            pages = models.Page.objects.filter(
                ocr__language_texts__language__code=language,
                issue__batch__name=batch
                ).values(
                    'reel__number', 'issue__date_issued', 'issue__title__lccn',
                    'issue__edition', 'sequence',
                ).order_by(
                    'reel__number', 'issue__title__lccn',
                    'issue__date_issued', 'sequence'
            )
            path = 'reports/language_batch_pages.html'
        paginator = Paginator(pages, 25)
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            page = paginator.page(1)
        page_range_short = list(_page_range_short(paginator, page))
    return render(request, path, locals())


def _title_range(reel):
    agg = models.Issue.objects.filter(pages__reel=reel).distinct().aggregate(
        mn=Min('date_issued'), mx=Max('date_issued'))
    if agg['mn'] and agg['mx']:
        mn = agg['mn'].strftime('%b %d, %Y')
        mx = agg['mx'].strftime('%b %d, %Y')
        return "%s - %s" % (mn, mx)
    else:
        return ""
