import os
import shutil
import hashlib
import tempfile
import tarfile
import datetime

from django.conf import settings
from django.test import TestCase
from django.utils import timezone

import core
from core.batch_loader import BatchLoader
from core.models import Batch, OcrDump

dumps_dir = settings.OCR_DUMP_STORAGE

class OcrDumpTests(TestCase):
    fixtures = ['test/countries.json', 'test/titles.json']

    @classmethod
    def setUpClass(cls):
        # Make sure TestCase does its setup (fixtures are loaded and whatnot)
        super(OcrDumpTests, cls).setUpClass()

        # Create temp directories for batch and ocr
        cls.batchDir = tempfile.mkdtemp()
        cls.dumpDir = tempfile.mkdtemp()
        settings.BATCH_STORAGE = cls.batchDir
        settings.OCR_DUMP_STORAGE = cls.dumpDir

        # Extract mini-batch tarball to batch dir
        tarpath = os.path.join(os.path.dirname(core.__file__), 'test-data', 'testbatch.tgz')
        tar = tarfile.open(tarpath)
        tar.extractall(path = cls.batchDir)
        tar.close()

    @classmethod
    def tearDownClass(cls):
        # Kill all temp files
        shutil.rmtree(cls.batchDir)
        shutil.rmtree(cls.dumpDir)

        # Make sure TestCase does its teardown, too
        super(OcrDumpTests, cls).tearDownClass()

    def test_ocr_dump(self):
        loader = BatchLoader()
        batch_dir = os.path.join(OcrDumpTests.batchDir, "batch_oru_testbatch_ver01")
        batch = loader.load_batch(batch_dir)
        self.assertEqual(batch.page_count, 27)

        t0 = timezone.now()

        dump = OcrDump.new_from_batch(batch)
        self.assertEqual(dump.name, "batch_oru_testbatch_ver01.tar.bz2")
        self.assertEqual(dump.path, os.path.join(OcrDumpTests.dumpDir, "batch_oru_testbatch_ver01.tar.bz2"))

        # make sure the sha1 looks good
        sha1 = hashlib.sha1()
        fh = open(dump.path, "rb")
        buff = fh.read()
        sha1.update(buff)
        self.assertEqual(dump.sha1, sha1.hexdigest())

        # make sure there are the right number of things in the dump
        t = tarfile.open(dump.path, "r:bz2")
        members = t.getmembers()
        self.assertEqual(len(members), 27 * 2) # ocr xml and txt for each page
        self.assertEqual(members[0].size, 19)

        # mtime on files in the archive should be just after we
        # created the OcrDump object from the batch
        t1 = datetime.datetime.fromtimestamp(members[0].mtime)
        t1 = timezone.make_aware(t1)
        self.assertTrue(t1 - t0 < datetime.timedelta(seconds=2))

        # Make sure the batch is gone - mysql gets purged between tests, but
        # solr does not.  This can't be done in teardown since the mysql db
        # is purged :(
        loader = BatchLoader()
        loader.purge_batch('batch_oru_testbatch_ver01')
