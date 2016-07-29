import os
from django.test import TestCase
import core
import datetime
from core.models import Copyright
from core.models import LccnDateCopyright
from core.load_copyright import loadCopyright
from core.load_copyright_map import loadCopyrightMap

class TestCopyrightLoaders(TestCase):

    def setUp(self):
        # wipe the slate clean
        Copyright.objects.all().delete()
        LccnDateCopyright.objects.all().delete()

        copyrighturis = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'copyrighturis.txt')
        loadCopyright(copyrighturis)

        lccnlist = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'lccnlist.txt')
        loadCopyrightMap(lccnlist)

        baddata1 = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'baddata1')
        f1 = open(baddata1, 'w')
        f1.write("http:/malformed.org/\tBad example\n")
        loadCopyright(baddata1)

        baddata2 = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'baddata2')
        f2 = open(baddata2, 'w')
        f2.write("sn11112222\t1/2/2002\t12/30/2006\thttp://creativecommons.org/licenses/by-nc-nd/4.0/")
        loadCopyright(baddata2)

        baddata3 = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'baddata3')
        f3 = open(baddata3, 'w')
        f3.write("sn33334444\t1976-01-01\t2002-01-01\thttp://www.europeana.eu/rights/rr-f/")
        loadCopyright(baddata3)

        os.remove(baddata1)
        os.remove(baddata2)
        os.remove(baddata3)

    def testCopyrightLoaders(self):
        issue_lccn = 'sn83045396'
        date_issued = "1911-03-15"
        date1 = datetime.date(1911, 1, 1)
        date2 = datetime.date(1911, 12, 31)
        rec1 = LccnDateCopyright.objects.filter(lccn = issue_lccn).filter(start_date__lt=date_issued).filter(end_date__gt=date_issued)
        self.assertEqual(rec1[0].lccn, 'sn83045396')
        self.assertEqual(rec1[0].start_date, date1)
        self.assertEqual(rec1[0].end_date, date2)
        self.assertEqual(rec1[0].copyright.uri, 'http://creativecommons.org/licenses/by-nc-nd/4.0/')
        self.assertEqual(rec1[0].copyright.label, 'Attribution-NonCommercial-NoDerivatives 4.0 International')

        lccn1 = 'sn11112222'
        lccn2 = 'sn33334444'
        baduri = "http:/malformed.org/"
        rec1 = None
        try:
            rec1 = LccnDateCopyright.objects.get(lccn=lccn1)
        except Exception as e:
            pass
        self.assertEqual(rec1, None)

        rec2 = None
        try:
            rec2 = LccnDateCopyright.objects.get(lccn=lccn2)
        except Exception as e:
            pass
        self.assertEqual(rec2, None)

        rec3 = None
        try:
            rec3 = Copyright.objects.get(uri=baduri)
        except Exception as e:
            pass
        self.assertEqual(rec3, None)
 

