from rfc3339 import rfc3339

import logging
_logger = logging.getLogger(__name__)

from django.core.management.base import BaseCommand
from django.core.paginator import Paginator
from django.db import reset_queries
from django.utils import timezone

from core import models as m
from core.rdf import rdf_uri

class Command(BaseCommand):
    help = "Indexes new batches in the sitemap"

    def handle(self, **options):
        write_sitemaps()


def write_sitemaps():
    """
    This function will write a sitemap index file that references individual
    sitemaps for all the batches, issues, pages and titles that have been
    loaded.
    """
    sitemap_index = open('static/sitemaps/sitemap.xml', 'w')
    sitemap_index.write('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')

    max_urls = 50000
    page_count = 0
    url_count = 0
    sitemap_file = None

    for loc, last_mod in sitemap_urls():

        # if we've maxed out the number of urls per sitemap 
        # close out the one we have open and open a new one
        if url_count % max_urls == 0:
            page_count += 1
            if sitemap_file:
                sitemap.write('</urlset>\n')
                sitemap.close()
            sitemap_file = 'sitemap-%05d.xml' % page_count
            sitemap_path = 'static/sitemaps/%s' % sitemap_file
            _logger.info("writing %s" % sitemap_path)
            sitemap = open(sitemap_path, 'w')
            sitemap.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
            sitemap_index.write('<sitemap><loc>%s/%s</loc></sitemap>\n' % (settings.BASE_URL, sitemap_file))

        # add a url to the sitemap
        sitemap.write("<url><loc>%s%s</loc><lastmod>%s</lastmod></url>\n" % (settings.BASE_URL, loc, rfc3339(last_mod)))
        url_count += 1

        # necessary to avoid memory bloat when settings.DEBUG = True
        if url_count % 1000 == 0:
            reset_queries()

    try:
        # wrap up some open files. do this only if we had release candidates 
        # if not, accessing sitemap variable will cause an error
        sitemap.write('</urlset>\n')
        sitemap.close()
    except NameError:
        _logger.info("No release candidates this time.")
        pass

    sitemap_index.write('</sitemapindex>\n')
    sitemap_index.close()

def sitemap_urls():
    """
    A generator that returns all the urls for batches, issues, pages and
    titles, and their respective modified time as a tuple.
    """
    for batch in m.Batch.objects.filter(sitemap_indexed__isnull=True):
        yield batch.url, batch.created
        yield rdf_uri(batch), batch.created
        batch.sitemap_indexed = timezone.now()
        batch.save()
        for issue in batch.issues.all():
            yield issue.url, batch.created
            yield rdf_uri(issue), batch.created
            for page in issue.pages.all():
                yield page.url, batch.created
                yield rdf_uri(page), batch.created

    paginator = Paginator(m.Title.objects.filter(sitemap_indexed__isnull=True), 10000)
    for page_num in range(1, paginator.num_pages + 1):
        page = paginator.page(page_num)
        for title in page.object_list:
            yield title.url, title.created
            title.sitemap_indexed = timezone.now()
            title.save()
