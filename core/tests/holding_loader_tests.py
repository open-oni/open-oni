import os.path

from django.test import TestCase

from core.models import Title
from core.title_loader import TitleLoader
from core.holding_loader import HoldingLoader

import core

class HoldingLoaderTests(TestCase):
    fixtures = ['test/countries.json', 'test/languages.json', 'test/institutions.json']

    def test_holdings(self):
        # title data
        titlexml = os.path.join(os.path.dirname(core.__file__), 
            'test-data', 'title.xml')

        # holdings data
        holdingsxml = os.path.join(os.path.dirname(core.__file__), 
            'test-data', 'holdings.xml')

        # first need to load the titles so we can link against them
        title_loader = TitleLoader()
        title_loader.load_file(titlexml)

        # now load the holdings from the same file
        holding_loader = HoldingLoader()
        holding_loader.load_file(holdingsxml)
        
        # fetch the title and see that holdings are attached
        t = Title.objects.get(lccn='sn83030846')
        holdings = list(t.holdings.all())
        self.assertEqual(len(holdings), 10)
        h = holdings[1]
        self.assertEqual(h.institution.name, 'Colgate Univ')
        self.assertEqual(h.type, 'Original')
        self.assertEqual(h.description, '<1876:5:18> <1884:1:10> <1885:9:3>')
        self.assertEqual(h.description_as_list(), [u'<1876:5:18>', u'<1884:1:10>', u'<1885:9:3>'])
        self.assertEqual(str(h.last_updated), '01/1992')
