import os
from django.test import TestCase
import core
from core.models import Copyright
from core.load_copyright import loadCopyright

class TestLoadCopyright(TestCase):

    def setUp(self):
        # wipe the slate clean
        Copyright.objects.all().delete()
        # load some uris

        copyrighturis = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'copyrighturis.txt')
        loadCopyright(copyrighturis)


    def testLoadCopyrights(self):
        copy1 = Copyright.objects.get(uri="http://creativecommons.org/publicdomain/mark/1.0/")
        self.assertEqual(copy1.label, 'Public Domain Mark 1.0')
