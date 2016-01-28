from datetime import date
import shutil
import os
import tempfile
import tarfile

from django.conf import settings
from django.test import TestCase

import openoni.core
from openoni.core.batch_loader import BatchLoader
from openoni.core.models import Title
from openoni.core.models import Batch

class BatchLoaderTest(TestCase):
    fixtures = ['countries.json', 'titles.json']

    @classmethod
    def setUpClass(cls):
      cls.batchDir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
      shutil.rmtree(cls.batchDir)

    def test_fixture(self):
        title = Title.objects.get(lccn = 'sn83030214')
        self.assertEqual(title.name, 'New-York tribune.')

    def test_load_batch(self):
        # Extract mini-batch tarball to /tmp somewhere
        tarpath = os.path.join(os.path.dirname(openoni.core.__file__), 'test-data', 'testbatch.tgz')
        tar = tarfile.open(tarpath)
        tar.extractall(path = BatchLoaderTest.batchDir)
        tar.close()
        settings.BATCH_STORAGE = BatchLoaderTest.batchDir

        batch_dir = os.path.join(BatchLoaderTest.batchDir, "batch_oru_testbatch_ver01")

        loader = BatchLoader(process_ocr=False)
        batch = loader.load_batch(batch_dir)
        self.assertTrue(isinstance(batch, Batch))
        self.assertEqual(batch.name, 'batch_oru_testbatch_ver01')
        self.assertEqual(len(batch.issues.all()), 4)

        title = Title.objects.get(lccn = 'sn83030214')
        self.assertTrue(title.has_issues)

        issue = batch.issues.all()[0]
        self.assertEqual(issue.volume, '1')
        self.assertEqual(issue.number, '1')
        self.assertEqual(issue.edition, 1)
        self.assertEqual(issue.title.lccn, 'sn83030214')
        self.assertEqual(date.strftime(issue.date_issued, '%Y-%m-%d'), '1999-06-15')
        self.assertEqual(len(issue.pages.all()), 15)

        page = issue.pages.all()[0]
        self.assertEqual(page.sequence, 1)
        self.assertEqual(page.url, u'/lccn/sn83030214/1999-06-15/ed-1/seq-1/')

        note = page.notes.all()[1]
        self.assertEqual(note.type, "noteAboutReproduction")
        self.assertEqual(note.text, "Present")

        # Validate page 1's metadata
        self.assertEqual(page.sequence, 1)
        self.assertEqual(page.jp2_filename, 'sn83030214/print/1999061501/0001.jp2')
        self.assertEqual(page.jp2_length, 411)
        self.assertEqual(page.jp2_width, 411)
        self.assertEqual(page.ocr_filename, 'sn83030214/print/1999061501/0001.xml')
        self.assertEqual(page.pdf_filename, 'sn83030214/print/1999061501/0001.pdf')

        # extract ocr data just for this page
        loader.process_ocr(page, index=False)
        self.assertTrue(page.ocr != None)
        self.assertTrue(len(page.ocr.text) > 0)

        p = Title.objects.get(lccn='sn83030214').issues.all()[0].pages.all()[0]
        self.assertTrue(p.ocr != None)

        # check that the solr_doc looks legit
        solr_doc = page.solr_doc
        self.assertEqual(solr_doc['id'], '/lccn/sn83030214/1999-06-15/ed-1/seq-1/')
        self.assertEqual(solr_doc['type'], 'page')
        self.assertEqual(solr_doc['sequence'], 1)
        self.assertEqual(solr_doc['lccn'], 'sn83030214')
        self.assertEqual(solr_doc['title'], 'New-York tribune.')
        self.assertEqual(solr_doc['date'], '19990615')
        self.assertEqual(solr_doc['batch'], 'batch_oru_testbatch_ver01')
        self.assertEqual(solr_doc['subject'], [
            u'New York (N.Y.)--Newspapers.',
            u'New York County (N.Y.)--Newspapers.'])
        self.assertEqual(solr_doc['place'], [
            u'New York--Brooklyn--New York City', 
            u'New York--Queens--New York City'])
        self.assertEqual(solr_doc['note'], [
            u"I'll take Manhattan",
            u'The Big Apple'])
        self.assertTrue(not solr_doc.has_key('essay'))
        self.assertEqual(solr_doc['ocr_eng'], 'LCCNsn83030214Page1')

        # purge the batch and make sure it's gone from the db
        loader.purge_batch('batch_oru_testbatch_ver01')
        self.assertEqual(Batch.objects.all().count(), 0)
        self.assertEqual(Title.objects.get(lccn='sn83030214').has_issues, False)
