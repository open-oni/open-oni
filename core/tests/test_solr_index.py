from django.test import TestCase
from django.conf import settings
from django.http import QueryDict as Q

from core import solr_index as si


class SolrIndexTests(TestCase):
    """
    Exercise some search form -> solr query translations
    """

    fixtures = ['test/ethnicities.json', 'test/languages.json']
    ocr_langs = ['ocr_%s' %l for l in settings.SOLR_LANGUAGES]


    # _expand_ethnicity (title)

    def test_expand_ethnicity(self):
        self.assertEqual(si._expand_ethnicity("Polish"), '(subject:"Polish" OR subject:"Poles" OR subject:"Polish Americans")')
        self.assertEqual(si._expand_ethnicity("French"), '(subject:"French" OR subject:"French Americans" OR subject:"French in South Carolina" OR subject:"French-American newspapers." OR subject:"French-Canadians")')


    # find_words (page)

    def test_find_words(self):
        hl = "Today <em>is</em> the <em>greatest</em> day i've <em>ever</em> known\nCan't wait <em>for</em> tomorrow ..."
        self.assertEqual(si.find_words(hl), ['is', 'greatest', 'ever',
            'for'])


    # _get_sort

    def test_get_sort(self):
        self.assertEqual(si._get_sort("state"), ("country", "asc"))
        self.assertEqual(si._get_sort("title"), ("title_normal", "asc"))
        self.assertEqual(si._get_sort("date", True), ("date", "asc"))
        self.assertEqual(si._get_sort("date"), ("start_year", "asc"))


    # index_titles

    # TODO reindex titles based on time one hour ago, etc
    # this would call index_title (could stub?)


    # index_pages

    # TODO index all pages in database, does not use a "since" time arg


    # page_count

    # TODO the below is pulling data from my development environment
    # commenting out until the test database is distinct

    # def test_page_count(self):
    #     self.assertEqual(si.page_count(), 131)


    # page_search

    def test_page_search_lccn(self):
        self.assertEqual(si.page_search(Q('lccn=sn83030214'))[0],
            '+type:page +lccn:("sn83030214")')
        self.assertEqual(si.page_search(Q('lccn=sn83030214&lccn=sn83030215'))[0],
            '+type:page +lccn:("sn83030214" "sn83030215")')

    def test_page_search_state(self):
        self.assertEqual(si.page_search(Q('state=California'))[0],
            '+type:page +state:("California")')
        self.assertEqual(si.page_search(Q('state=California&state=New Jersey'))[0],
            '+type:page +state:("California" "New Jersey")')

    def test_page_search_year(self):
        self.assertEqual(si.page_search(Q('yearRange=1900'))[0],
            '+type:page +year:[1900 TO 1900]')

    def test_page_search_year_range(self):
        self.assertEqual(si.page_search(Q('yearRange=1900-1915'))[0],
            '+type:page +year:[1900 TO 1915]')

    def test_page_search_date_range(self):
        self.assertEqual(
            si.page_search(Q('date1=1901-10-25&date2=1901-10-31'))[0],
            '+type:page +date:[19011025 TO 19011031]')

    def test_page_search_date1_only(self):
        self.assertEqual(
            si.page_search(Q('date1=1988-05-30&date2='))[0],
            '+type:page +date:[19880530 TO *]')

    def test_page_search_date2_only(self):
        self.assertEqual(
            si.page_search(Q('date2=1880-01-07'))[0],
            '+type:page +date:[* TO 18800107]')

    def test_page_search_year_range_and_dates(self):
        self.assertEqual(
            si.page_search(Q('date1=1900-01-01&date2=1910-12-31&yearRange=1902-1904'))[0],
            '+type:page +year:[1902 TO 1904]')

    def test_page_search_no_date(self):
        self.assertEqual(
            si.page_search(Q('date1&date2'))[0],
            '+type:page')

    # TODO not sure that the or / and / prox / text texts are searching languages correctly
    # see coverage report for page_search function

    def test_page_search_ortext(self):
        q = ' OR '.join(['%s:("apples" "oranges")' % lang for lang in self.ocr_langs])
        self.assertEqual(si.page_search(Q('ortext=apples%20oranges'))[0], u'+type:page +((ocr:("apples" "oranges")^10000 ) OR %s )' % q)

    def test_page_search_andtext(self):
        q = ' OR '.join(['%s:(+"apples" +"oranges")' % lang for lang in self.ocr_langs])
        self.assertEqual(si.page_search(Q('andtext=apples%20oranges'))[0], u'+type:page +((ocr:(+"apples" +"oranges")^10000 ) OR %s )' % q)

    def test_page_search_phrase(self):
        q = ' OR '.join(['%s:"new york yankees"' % lang for lang in self.ocr_langs])
        self.assertEqual(si.page_search(Q('phrasetext=new%20york%20yankees'))[0], u'+type:page +((ocr:"new york yankees"^10000 ) OR %s )' % q)

    def test_page_search_proxtext(self):
        q = ' OR '.join(['%s:"apples oranges"~10' % lang for lang in self.ocr_langs])
        self.assertEqual(si.page_search(Q('proxtext=apples%20oranges&proxdistance=10'))[0], u'+type:page +((ocr:("apples oranges"~10)^10000 ) OR %s )' %q)
        q = ' OR '.join(['%s:"apples oranges"~5' % lang for lang in self.ocr_langs])
        self.assertEqual(si.page_search(Q('proxtext=apples%20oranges'))[0], u'+type:page +((ocr:("apples oranges"~5)^10000 ) OR %s )' %q)

    def test_page_search_language(self):
        self.assertEqual(si.page_search(Q('proxtext=apples%20oranges&language=English'))[0], '+type:page +language:English +((ocr:("apples oranges"~5)^10000 AND ocr_eng:"apples oranges"~5 ) OR ocr_eng:"apples oranges"~5 )')

    # TODO can add tests for faceting once there is a solr test environment

    # query_join (page)
    
    def test_query_join(self):
        self.assertEqual(si.query_join(["Nebraska", "New York"], "state"), '+state:("Nebraska" "New York")')
        self.assertEqual(si.query_join("Nebraska", "state"), '+state:("Nebraska")')


    # _solrize_date

    def test_solrize_date(self):
        self.assertEqual(si._solrize_date('1900-03-01'), "19000301")
        self.assertEqual(si._solrize_date('1900'), "*")
        self.assertEqual(si._solrize_date('1900-01'), "*")
        self.assertEqual(si._solrize_date('1900'), "*")
        self.assertEqual(si._solrize_date('1900'), "*")


    # _solr_escape (page)
    
    def test_solr_escape(self):
        self.assertEqual(si._solr_escape('New+York'), 'New\+York')
        self.assertEqual(si._solr_escape('New\York'), 'New\\York')
        # TODO add more tests for escaping


    # title_count

    # TODO the below is pulling titles from my development environment
    # commenting out until test and development db issue resolved

    # def test_title_count(self):
    #     self.assertEqual(si.title_count(), 3)


    # title_search

    def test_title_search(self):
        self.assertEqual(
            si.title_search(Q('terms=bloody'))[0], 
            '+type:title +(title:"bloody" OR essay:"bloody" OR note:"bloody" OR edition:"bloody" OR place_of_publication:"bloody" OR url:"bloody" OR publisher:"bloody")')
        self.assertEqual(len(si.title_search(Q('state=New+York'))), 2)

    def test_ethnicity_query(self):
        self.assertEqual(si.title_search(Q('ethnicity=Anabaptist'))[0], 
                '+type:title +(subject:"Anabaptist" OR subject:"Amish" OR subject:"Amish Mennonites" OR subject:"Mennonites" OR subject:"Pennsylvania Dutch" OR subject:"Pennsylvania Dutch.")')
