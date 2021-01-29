from django.test import TestCase
from core.models import Issue, Copyright
import datetime

class IssueCopyrightTests(TestCase):
    # With no copyrights in the database, pulling a PD issue's link creates one
    def test_empty_db_pd_issue_has_copyright_link(self):
        self.assertEqual(Copyright.objects.count(), 0)
        # This is the absolute latest an issue can be considered public domain
        i = Issue(date_issued = datetime.date(datetime.date.today().year - 96, 12, 31))
        c = i.copyright_link
        self.assertEqual(Copyright.objects.count(), 1)
        dbc = Copyright.objects.all()[0]

        # Make sure what got stuffed in the DB is the same as what got returned
        # since the return is created on the fly.
        self.assertEqual(c.label, dbc.label)
        self.assertEqual(c.uri, dbc.uri)

        # Next we make sure label and URI aren't empty.  We don't hard-code the
        # expected label/uri, we just want to be sure they exist.
        self.assertTrue(len(c.label) > 10)
        self.assertTrue(len(c.uri) > 10)

    def test_non_pd_issue_has_no_copyright_link(self):
        # This is the absolute earliest an issue can be non-PD
        i = Issue(date_issued = datetime.date(datetime.date.today().year - 95, 1, 1))
        c = i.copyright_link
        # No copyright
        self.assertTrue(c is None)
        # No link is created in the db
        self.assertEqual(Copyright.objects.count(), 0)

    def test_we_dont_make_multiple_links(self):
        self.assertEqual(Copyright.objects.count(), 0)
        i1 = Issue(date_issued = datetime.date(1800, 1, 1))
        c1 = i1.copyright_link
        self.assertEqual(Copyright.objects.count(), 1)
        dbc1 = Copyright.objects.all()[0]

        i2 = Issue(date_issued = datetime.date(1801, 1, 1))
        c2 = i2.copyright_link
        self.assertEqual(Copyright.objects.count(), 1)

        self.assertEqual(c1.uri, c2.uri)
        self.assertEqual(c1.label, c2.label)
