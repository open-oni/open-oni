import os

from django.conf.urls import url
from django.conf import settings
from django.utils import cache

from .views import home, browse, directory, reports, search, static

handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'


def cache_page(function, ttl):
    def decorated_function(*args, **kwargs):
        request = args[0]
        response = function(*args, **kwargs)
        cache.patch_response_headers(response, ttl)
        cache.patch_cache_control(response, public=True)
        return response
    return decorated_function

urlpatterns = [
    url(r'^$',
        cache_page(home.home, settings.DEFAULT_TTL_SECONDS),
        name="openoni_home"),
    url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$',
        cache_page(home.home, settings.DEFAULT_TTL_SECONDS),
        name="openoni_home_date"),
    url(r'^frontpages/(?P<date>\d{4}-\d{1,2}-\d{1,2}).json$',
        cache_page(home.frontpages, settings.DEFAULT_TTL_SECONDS),
        name="openoni_frontpages_date_json"),

    # Served direct by Apache, but Django needs to provide reversed URL
    # as data-coordinates_url attribute in page.html, thus 'static.empty' view
    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4/coordinates/
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)/coordinates/$',
        static.empty, name="openoni_page_coordinates"),

    url(r'^about/$', static.about, name="openoni_about"),

    url(r'^help/$', static.help, name="openoni_help"),

    # explainOCR.html
    url(r'^ocr/$', reports.ocr, name="openoni_ocr"),

    # API docs
    url(r'^about/api/$', static.about_api, name="openoni_about_api"),

    # example: /lccn/sn85066387
    url(r'^lccn/(?P<lccn>\w+)/$', browse.title, name="openoni_title"),

    # example: /issues/
    url(r'^issues/$', browse.issues, name="openoni_issues"),

    # example: /issues/1900
    url(r'^issues/(?P<year>\d{4})$', browse.issues, name="openoni_issues_for_year"),

    # example: /lccn/sn85066387/issues/
    url(r'^lccn/(?P<lccn>\w+)/issues/$', browse.issues_title, name="openoni_issues_title"),

    # example: /lccn/sn85066387/issues/1900
    url(r'^lccn/(?P<lccn>\w+)/issues/(?P<year>\d{4})/$',
       browse.issues_title, name="openoni_issues_title_for_year"),

    # example: /lccn/sn85066387/issues/first_pages
    url(r'^lccn/(?P<lccn>\w+)/issues/first_pages/$', browse.issues_first_pages,
        name="openoni_issues_first_pages"),

    # example: /lccn/sn85066387/issues/first_pages/3
    url(r'^lccn/(?P<lccn>\w+)/issues/first_pages/(?P<page_number>\d+)/$',
        browse.issues_first_pages, name="openoni_issues_first_pages_page_number"),

    # example: /lccn/sn85066387/marc
    url(r'^lccn/(?P<lccn>\w+)/marc/$', browse.title_marc,
        name="openoni_title_marc"),

    # example: /lccn/sn85066387/feed/
    url(r'^lccn/(?P<lccn>\w+)/feed/$', browse.title_atom,
        name='openoni_title_atom'),

    # example: /lccn/sn85066387/feed/10
    url(r'^lccn/(?P<lccn>\w+)/feed/(?P<page_number>\w+)$', browse.title_atom,
        name='openoni_title_atom_page'),

    # example: /lccn/sn85066387/marc.xml
    url(r'^lccn/(?P<lccn>\w+)/marc.xml$', browse.title_marcxml,
        name="openoni_title_marcxml"),

    # example: /lccn/sn85066387/holdings
    url(r'^lccn/(?P<lccn>\w+)/holdings/$', browse.title_holdings,
        name="openoni_title_holdings"),

    # example: /essays/
    url(r'^essays/$', reports.essays, name='openoni_essays'),

    # example: /essays/1/
    url(r'^essays/(?P<essay_id>\d+)/$', reports.essay, name='openoni_essay'),

    # TOD0: remove this some suitable time after 08/2010 since it
    # permanently redirects to new essay id based URL
    # example: /lccn/sn85066387/essay
    url(r'^lccn/(?P<lccn>\w+)/essays/$', browse.title_essays,
        name="openoni_title_essays"),

    # example: /lccn/sn85066387/1907-03-17/ed-1
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/$',
        browse.issue_pages, name="openoni_issue_pages"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/1
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/(?P<page_number>\d+)/$',
        browse.issue_pages, name="openoni_issue_pages_page_number"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)/$',
        browse.page, name="openoni_page"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4.pdf
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+).pdf$',
        browse.page_pdf, name="openoni_page_pdf"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4.jp2
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+).jp2$',
        browse.page_jp2, name="openoni_page_jp2"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4/ocr.xml
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)/ocr.xml$',
        browse.page_ocr_xml, name="openoni_page_ocr_xml"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4/ocr.txt
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)/ocr.txt$',
        browse.page_ocr_txt, name="openoni_page_ocr_txt"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4/;words=
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)/;words=(?P<words>.+)$',
        browse.page, name="openoni_page_words"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4/print/image_813x1024_from_0,0_to_6504,8192
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)/print/image_(?P<width>\d+)x(?P<height>\d+)_from_(?P<x1>\d+),(?P<y1>\d+)_to_(?P<x2>\d+),(?P<y2>\d+)/$',
    browse.page_print, name="openoni_page_print"),

    # example: /lccn/sn85066387/1907-03-17/ed-1/seq-4/ocr/
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)/ocr/$',
        browse.page_ocr, name="openoni_page_ocr"),

    url(r'^newspapers/$', directory.newspapers, name='openoni_newspapers'),
    url(r'^newspapers/feed/$', directory.newspapers_atom, name='openoni_newspapers_atom'),

    url(r'^newspapers.(?P<format>json)$', directory.newspapers,
        name='openoni_newspapers_format'),

    url('search/pages/opensearch.xml', search.search_pages_opensearch,
        name='openoni_search_pages_opensearch'),
    url(r'^search/pages/results/$', search.search_pages_results,
        name='openoni_search_pages_results'),
    url(r'^search/pages/results/(?P<view_type>list)/$', search.search_pages_results,
        name='openoni_search_pages_results_list'),

    url('search/titles/opensearch.xml', search.search_titles_opensearch,
        name='openoni_search_titles_opensearch'),
    url(r'^search/titles/$', search.search_titles,
        name='openoni_search_titles'),
    url(r'^search/titles/results/$', directory.search_titles_results,
        name='openoni_search_titles_results'),
    url(r'^suggest/titles/$', search.suggest_titles,
        name='openoni_suggest_titles'),

    url(r'^search/pages/navigation/$', search.search_pages_navigation,
        name='openoni_search_pages_navigation'),

    url(r'^search/advanced/$', search.search_advanced,
        name='openoni_search_advanced'),

    url(r'^events/$', reports.events, name='openoni_events'),
    url(r'^events\.csv$', reports.events_csv, name='openoni_events_csv'),
    url(r'^events/(?P<page_number>\d+)/$', reports.events,
        name='openoni_events_page'),
    url(r'^events/feed/$', reports.events_atom, name='openoni_events_atom'),
    url(r'^events/feed/(?P<page_number>\d+)/$', reports.events_atom,
        name='openoni_events_atom_page'),
    url(r'^event/(?P<event_id>.+)/$', reports.event, name='openoni_event'),
    url(r'^awardees/$', reports.awardees, name='openoni_awardees'),
    url(r'^awardees.json$', reports.awardees_json, name='openoni_awardees_json'),

    # example: /titles
    url(r'^titles/$', browse.titles, name='openoni_titles'),

    # example: /titles;page=5
    url(r'^titles/;page=(?P<page_number>\d+)$', browse.titles,
            name='openoni_titles_page'),

    # example: /titles;start=F
    url(r'^titles/;start=(?P<start>\w)$', browse.titles, name='openoni_titles_start'),

    # example: /titles;start=F;page=5
    url(r'^titles/;start=(?P<start>\w);page=(?P<page_number>\d+)$',
        browse.titles, name='openoni_titles_start_page'),

    # example: /titles/places/pennsylvania
    url(r'^titles/places/(?P<state>[^/;]+)/$', browse.titles_in_state,
        name='openoni_state'),

    # example: /titles/places/pennsylvania;page=1
    url(r'^titles/places/(?P<state>[^/;]+)/;page=(?P<page_number>\d+)$',
        browse.titles_in_state, name='openoni_state_page_number'),

    # example: /titles/places/pennsylvania;page=1;order=title
    url(r'^titles/places/(?P<state>[^;]+)/;page=(?P<page_number>\d+);(?P<order>\w+)$',
        browse.titles_in_state, name='openoni_state_page_number'),

    # example /titles/places/pennsylvania/allegheny
    url(r'^titles/places/(?P<state>[^/;]+)/(?P<county>[^/;]+)/$',
        browse.titles_in_county, name='openoni_county'),

    # example /titles/places/pennsylvania/allegheny;page=1
    url(r'^titles/places/(?P<state>[^/;]+)/(?P<county>[^/;]+)/;page=(?P<page_number>\d+)$',
        browse.titles_in_county, name='openoni_county_page_number'),

    # example: /titles/places/pennsylvania/allegheny/pittsburgh
    url(r'^titles/places/(?P<state>[^/;]+)/(?P<county>[^/;]+)/(?P<city>[^/;]+)/$',
        browse.titles_in_city, name='openoni_city'),

    # example: /titles/places/pennsylvania/allegheny/pittsburgh;page=1
    url(r'^titles/places/(?P<state>[^/;]+)/(?P<county>[^/]+)/(?P<city>[^/;]+)/;page=(?P<page_number>\d+)$',
        browse.titles_in_city, name='openoni_city_page_number'),

    # example: # /titles/places/pennsylvania/allegheny/pittsburgh;page=1;order=title
    url(r'^titles/places/(?P<state>[^/;]+)/(?P<county>[^/;]+)/(?P<city>[^/;]+)/;page=(?P<page_number>\d+);(?P<order>\w+)$',
        browse.titles_in_city, name='openoni_city_page_number'),

    # example: /states
    url(r'^states/$', reports.states, name='openoni_states'),

    # example: /states_counties/
    url(r'^states_counties/$', reports.states_counties, name='openoni_states_counties'),

    # example: /states.json
    url(r'^states\.(?P<format>json)$', reports.states, name='openoni_states_json'),

    # example: /counties/pennsylvania
    url(r'^counties/(?P<state>[^/;]+)/$', reports.counties_in_state, name='openoni_counties_in_state'),

    # example: /counties/pennsylvania.json
    url(r'^counties/(?P<state>[^/;]+)\.(?P<format>json)$', reports.counties_in_state, name='openoni_counties_in_state_json'),

    # example: /cities/pennsylvania/allegheny
    url(r'^cities/(?P<state>[^/;]+)/(?P<county>[^/]+)/$', reports.cities_in_county, name='openoni_cities_in_county'),

    # example: /cities/pennsylvania/allegheny.json
    url(r'^cities/(?P<state>[^/;]+)/(?P<county>[^/]+)\.(?P<format>json)$', reports.cities_in_county, name='openoni_cities_in_county_json'),

    # example: /cities/pennsylvania
    url(r'^cities/(?P<state>[^/;]+)/$', reports.cities_in_state, name='openoni_cities_in_state'),

    # example: /cities/pennsylvania.json
    url(r'^cities/(?P<state>[^/;]+)\.(?P<format>json)$', reports.cities_in_state, name='openoni_cities_in_state_json'),

    # example: /institutions
    url(r'^institutions/$', reports.institutions, name='openoni_institutions'),

    # example: /institutions;page=5
    url(r'^institutions/;page=(?P<page_number>\d+)$', reports.institutions,
        name='openoni_institutions_page_number'),

    # example: /institutions/cuy
    url(r'^institutions/(?P<code>[^/]+)/$', reports.institution,
        name='openoni_institution'),

    # example: /institutions/cuy/titles
    url(r'^institutions/(?P<code>[^/]+)/titles/$', reports.institution_titles,
        name='openoni_institution_titles'),

    # example: /institutions/cuy/titles/5/
    url(r'^institutions/(?P<code>[^/]+)/titles/(?P<page_number>\d+)/$',
        reports.institution_titles, name='openoni_institution_titles_page_number'),

    # awardee
    url(r'^awardees/(?P<institution_code>\w+)/$', reports.awardee,
        name='openoni_awardee'),
    url(r'^awardees/(?P<institution_code>\w+).json$', reports.awardee_json, name='openoni_awardee_json'),


    url(r'^status', reports.status, name='openoni_stats'),

# linked-data rdf/atom/json views

    # newspapers
    url(r'^newspapers.rdf$', directory.newspapers_rdf, name="openoni_newspapers_dot_rdf"),
    url(r'^newspapers$', directory.newspapers_rdf, name="openoni_newspapers_rdf"),

    # title
    url(r'^lccn/(?P<lccn>\w+).rdf$', browse.title_rdf, name='openoni_title_dot_rdf'),
    url(r'^lccn/(?P<lccn>\w+)$', browse.title_rdf, name='openoni_title_rdf'),
    url(r'^lccn/(?P<lccn>\w+).json', reports.title_json, name='openoni_title_dot_json'),

    # issue
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+).rdf$', browse.issue_pages_rdf, name='openoni_issue_pages_dot_rdf'),
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+).json$', reports.issue_pages_json, name='openoni_issue_pages_dot_json'),
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)$', browse.issue_pages_rdf, name='openoni_issue_pages_rdf'),

    # page
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+).rdf$', browse.page_rdf, name="openoni_page_dot_rdf"),
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+).json$', reports.page_json, name="openoni_page_dot_json"),
    url(r'^lccn/(?P<lccn>\w+)/(?P<date>\d{4}-\d{2}-\d{2})/ed-(?P<edition>\d+)/seq-(?P<sequence>\d+)$', browse.page_rdf, name="openoni_page_rdf"),

    # awardee
    url(r'^awardees/(?P<institution_code>\w+).rdf$', reports.awardee_rdf, name='openoni_awardee_dot_rdf'),
    url(r'^awardees/(?P<institution_code>\w+)$', reports.awardee_rdf, name='openoni_awardee_rdf'),

    # ndnp vocabulary
    url(r'^terms/.*$', reports.terms, name='openoni_terms'),

    # batch summary
    url(r'^batches/summary/$', reports.batch_summary, name='openoni_batch_summary'),
    url(r'^batches/summary.(?P<format>txt)$', reports.batch_summary,
        name='openoni_batch_summary_txt'),

    # batch view
    url(r'^batches/$', reports.batches, name='openoni_batches'),
    url(r'^batches/;page=(?P<page_number>\d+)$', reports.batches,
        name='openoni_batches_page'),
    url(r'^batches/feed/$', reports.batches_atom, name='openoni_batches_atom'),
    url(r'^batches/feed/(?P<page_number>\d+)/$',reports.batches_atom,
        name='openoni_batches_atom_page'),
    url(r'^batches\.json$', reports.batches_json, name='openoni_batches_json'),
    url(r'^batches\.csv$', reports.batches_csv, name='openoni_batches_csv'),
    url(r'^batches/(?P<batch_name>.+)/$', reports.batch, name='openoni_batch'),
    url(r'^batches/(?P<batch_name>.+).rdf$', reports.batch_rdf,
        name='openoni_batch_dot_rdf'),
    url(r'^batches/(?P<batch_name>.+)\.json$', reports.batch_json,
        name='openoni_batch_dot_json'),
    url(r'^batches/(?P<batch_name>.+)$', reports.batch_rdf, name='openoni_batch_rdf'),

    # reels
    url(r'^reels/$', reports.reels, name='openoni_reels'),
    url(r'^reels/;page=(?P<page_number>\d+)$', reports.reels,
        name='openoni_reels_page'),
    url(r'^reel/(?P<reel_number>\w+)/$', reports.reel, name='openoni_reel'),

    # languages
    url(r'^languages/$', reports.languages, name='openoni_languages'),
    url(r'^languages/(?P<language>.+)/batches/$', reports.language_batches,
        name='openoni_language_batches'),
    url(r'^languages/(?P<language>.+)/batches/;page=(?P<page_number>\d+)$', reports.language_batches,
        name='openoni_language_batches_page_number'),
    url(r'^languages/(?P<language>.+)/titles/$', reports.language_titles,
        name='openoni_language_titles'),
    url(r'^languages/(?P<language>.+)/titles/;page=(?P<page_number>\d+)$', reports.language_titles,
        name='openoni_language_titles_page_number'),
    url(r'^languages/(?P<language>.+)/(?P<batch>.+)/(?P<title>.+)/$', reports.language_pages,
        name='openoni_language_title_pages'),
    url(r'^languages/(?P<language>.+)/(?P<batch>.+)/(?P<title>.+)/;page=(?P<page_number>\d+)$', reports.language_pages,
        name='openoni_language_title_pages_page_number'),
    url(r'^languages/(?P<language>.+)/(?P<batch>.+)/$', reports.language_pages,
        name='openoni_language_batch_pages'),
    url(r'^languages/(?P<language>.+)/(?P<batch>.+)/;page=(?P<page_number>\d+)$', reports.language_pages,
        name='openoni_language_batch_pages_page_number'),

    # reports
    url(r'^reports/$', reports.reports, name='openoni_reports'),

    # ocr data
    url(r'^ocr/feed/$', reports.ocr_atom, name='openoni_ocr_atom'),
    url(r'^ocr.json$', reports.ocr_json, name='openoni_ocr_json'),
]
