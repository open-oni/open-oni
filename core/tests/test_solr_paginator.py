from django.test import TestCase
from django.conf import settings
from django.http import QueryDict

from core import solr_index

class SolrPaginatorTests(TestCase):
    fixtures = ['test/countries.json', 'test/awardee.json', 'test/titles.json',
                'test/many_pages.json', 'test/ethnicities.json', 'test/languages.json']

    def test_count(self):
        solr = solr_index.conn()
        solr.delete(q='type:page')
        solr_index.index_pages()
        solr.commit()
        self.assertEqual(solr_index.page_count(), 108)

        q = QueryDict('proxtext=')
        p = solr_index.SolrPaginator(q)
        self.assertEqual(108, p.count)
