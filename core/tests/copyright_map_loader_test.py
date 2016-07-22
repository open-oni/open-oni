from django.test import TestCase
from openoni.core.models import LccnDateCopyright
from openoni.core.load_copyright_map import loadCopyrightMap

class LoadCopyrightMapTests(TestCase):

    def setUp(self):
        # wipe the slate clean
        LccnDateCopyright.objects.all().delete()
        # load some uris

        lccnlist = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'lccnlist.txt')
        loadCopyrightMap(lccnlist)


    def testLoadCopyrightMaps(self):
        issue_lccn = 'sn83045396'
        date_issued = 1911-03-15 
        rec1 = LccnDateCopyright.objects.filter(lccn = issue_lccn).filter(start_date__lt=date_issued).filter(end_date__gt=date_issued)
        self.assertEqual(rec1.lccn, 'sn83045396')
        self.assertEqual(rec1.startDate, 1911-01-01)
        self.assertEqual(rec1.endDate, 1911-12-31)
        self.assertEqual(rec1.uri.uri, 'http://creativecommons.org/licenses/by-nc-nd/4.0/')
