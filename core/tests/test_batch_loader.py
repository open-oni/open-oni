import shutil
import os
import tempfile
import tarfile
from datetime import datetime
from unittest.mock import patch

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

import core
from core.batch_loader import BatchLoader
from core.models import Batch, Job, Title


# `timezone.now` will now always return the value we want
# Note this also sets the same last_modified value of all Job records
@patch(
    "django.utils.timezone.now",
    lambda: datetime(2011, 3, 11, tzinfo=timezone.utc),
)

class BatchLoaderTest(TestCase):
    fixtures = [
        'test/countries.json',
        'test/languages.json',
        'test/titles.json'
    ]

    @classmethod
    def setUpClass(cls):
        # Make sure TestCase does its setup (fixtures are loaded and whatnot)
        super(BatchLoaderTest, cls).setUpClass()

        cls.batchDir = tempfile.mkdtemp()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.batchDir)

        # Make sure TestCase does its teardown, too
        super(BatchLoaderTest, cls).tearDownClass()

    def test_fixture(self):
        title = Title.objects.get(lccn = 'sn83030214')
        self.assertEqual(title.name, 'New-York tribune.')

    def test_load_batch(self):
        # Extract mini-batch tarball to /tmp somewhere
        tarpath = os.path.join(os.path.dirname(core.__file__), 'test-data', 'testbatch.tgz')
        tar = tarfile.open(tarpath)
        tar.extractall(path = BatchLoaderTest.batchDir)
        tar.close()
        settings.BATCH_STORAGE = BatchLoaderTest.batchDir

        batch_name = 'batch_oru_testbatch_ver01'
        batch_dir = os.path.join(BatchLoaderTest.batchDir, batch_name)

        loader = BatchLoader(process_ocr=False)

        # Test loading a batch that doesn't exist
        nonexistent_batch_name = 'batch_nbu_nonexistent_ver01'
        nonexistent_batch_path = os.path.join(BatchLoaderTest.batchDir, nonexistent_batch_name)
        batch = loader.load_batch(nonexistent_batch_path)
        self.assertEqual(Batch.objects.all().count(), 0)

        # Test non-interactive load of batch that doesn't exist
        with self.assertRaisesMessage(core.batch_loader.BatchLoaderException,
                                      "Unable to load %s: could not find batch_1.xml (or any of its aliases) in '%s/data/' -- has the batch been validated?" % (nonexistent_batch_path, nonexistent_batch_path)):
            batch = loader.load_batch(nonexistent_batch_path, interactive=False)
        self.assertEqual(Batch.objects.all().count(), 0)

        # Add fake in progress load_batch to test blocking jobs on same batch
        fake_batch_job = Job(
            info=batch_name,
            status=Job.Status.IN_PROGRESS,
            type=Job.Type.LOAD_BATCH,
        )
        fake_batch_job.save()

        # Try to start a new load_batch job with the same batch
        with self.assertRaisesMessage(core.batch_loader.BatchLoaderException,
                                      "Job for batch %s already in progress:" % batch_name):
            batch = loader.load_batch(batch_dir)
        self.assertEqual(Batch.objects.all().count(), 0)

        # Change fake job to purge_batch to check it still blocks new load_batch
        fake_batch_job.type = Job.Type.PURGE_BATCH
        fake_batch_job.save()
        with self.assertRaisesMessage(core.batch_loader.BatchLoaderException,
                                      "Job for batch %s already in progress:" % batch_name):
            batch = loader.load_batch(batch_dir)
        self.assertEqual(Batch.objects.all().count(), 0)

        # Change fake job to FAILED so it no longer blocks load_batch
        fake_batch_job.status = Job.Status.FAILED
        fake_batch_job.save()

        batch = loader.load_batch(batch_dir)
        self.assertTrue(isinstance(batch, Batch))
        self.assertEqual(batch.name, batch_name)
        self.assertEqual(batch.completed_at, timezone.now())
        self.assertEqual(len(batch.issues.all()), 4)
        self.assertEqual(
            Job.objects.filter(type=Job.Type.LOAD_BATCH, info=batch.name).first().status,
            Job.Status.SUCCEEDED
        )
        # Job table now has successful load_batch and failed purge_batch records

        title = Title.objects.get(lccn = 'sn83030214')
        self.assertTrue(title.has_issues)

        issue = batch.issues.all()[0]
        self.assertEqual(issue.volume, '1')
        self.assertEqual(issue.number, '1')
        self.assertEqual(issue.edition, 1)
        self.assertEqual(issue.title.lccn, 'sn83030214')
        self.assertEqual(issue.date_issued.strftime('%Y-%m-%d'), '1999-06-15')
        self.assertEqual(len(issue.pages.all()), 15)

        page = issue.pages.all()[0]
        self.assertEqual(page.sequence, 1)
        self.assertEqual(page.url, '/lccn/sn83030214/1999-06-15/ed-1/seq-1/')

        notes = page.notes.order_by("type").all()
        self.assertEqual(len(notes), 2)
        note = page.notes.all()[0]
        self.assertEqual(note.type, "noteAboutReproduction")
        self.assertEqual(note.text, "Present")
        note = page.notes.all()[1]
        self.assertEqual(note.type, "agencyResponsibleForReproduction")
        self.assertEqual(note.text, "oru")

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
        self.assertEqual(solr_doc['batch'], batch_name)
        self.assertEqual(solr_doc['subject'], [
            'New York (N.Y.)--Newspapers.',
            'New York County (N.Y.)--Newspapers.'])
        self.assertEqual(solr_doc['place'], [
            'New York--Brooklyn--New York City', 
            'New York--Queens--New York City'])
        self.assertEqual(solr_doc['note'], [
            "I'll take Manhattan",
            'The Big Apple'])
        self.assertTrue('essay' not in solr_doc)
        self.assertEqual(solr_doc['ocr_eng'], 'LCCNsn83030214Page1')

        # Change fake purge job back to IN_PROGRESS to block purge of same batch
        fake_batch_job.status = Job.Status.IN_PROGRESS
        fake_batch_job.save()

        # Try to start a new purge_batch job with the same batch
        with self.assertRaisesMessage(core.batch_loader.BatchLoaderException,
                                      "Job for batch %s already in progress:" % batch_name):
            loader.purge_batch(batch_name)
        self.assertEqual(Batch.objects.all().count(), 1)

        # Change fake job to load_batch to check it still blocks new purge_batch
        fake_batch_job.type = Job.Type.LOAD_BATCH
        fake_batch_job.save()
        with self.assertRaisesMessage(core.batch_loader.BatchLoaderException,
                                      "Job for batch %s already in progress:" % batch_name):
            loader.purge_batch(batch_name)
        self.assertEqual(Batch.objects.all().count(), 1)

        # Change fake job to FAILED so it no longer blocks purge_batch
        fake_batch_job.status= Job.Status.FAILED
        fake_batch_job.save()

        # Test purging a batch that doesn't exist
        with self.assertRaisesMessage(core.batch_loader.BatchLoaderException,
                                      "Tried to purge batch that does not exist: %s" % nonexistent_batch_name):
            loader.purge_batch(nonexistent_batch_name)
        self.assertEqual(Batch.objects.all().count(), 1)

        # Test non-interactive purging a batch that doesn't exist
        with patch.object(BatchLoader, '_purge_batch',
                          side_effect=RuntimeError('Something failed with purging the batch.')):
            with self.assertRaisesMessage(core.batch_loader.BatchLoaderException,
                                          "Purge of %s failed: Something failed with purging the batch." % batch_name):
                loader.purge_batch(batch_name, interactive=False)
        self.assertEqual(Batch.objects.all().count(), 1)
        # Delete failed job so doesn't interfere with job assertion below
        Job.objects.filter(type=Job.Type.PURGE_BATCH, info=batch.name).delete()

        # purge the batch and make sure it's gone from the db and job succeeded
        loader.purge_batch(batch_name)
        self.assertEqual(Batch.objects.all().count(), 0)
        self.assertEqual(Title.objects.get(lccn='sn83030214').has_issues, False)
        self.assertEqual(
            Job.objects.filter(type=Job.Type.PURGE_BATCH, info=batch.name).first().status,
            Job.Status.SUCCEEDED
        )
