from django.test import TestCase
from openoni.core.models import Copyright
from openoni.core.load_copyright import loadCopyright

class LoadCopyrightTest(TestCase):

    def setUp(self):
        # wipe the slate clean
        Copyright.objects.all().delete()
        # load some uris

        copyrighturis = os.path.join(os.path.dirname(core.__file__),
            'test-data', 'copyrighturis.txt')
        loadCopyright(copyrighturis)


    def testLoadCopyrights(self):
        copy1 = Copyright.objects.get("http://creativecommons.org/publicdomain/mark/1.0/")
        self.assertEqual(t.label, 'Public Domain Mark 1.0')
