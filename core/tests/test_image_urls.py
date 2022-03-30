import os
import core
from django.test import TestCase
from core.models import Page
from core.utils import image_urls

class ImageUrlsTests(TestCase):
    fixtures = [
        'test/batch.json',
        'test/issue.json',
        'test/page.json',
        'test/reel.json',
        'test/titles.json'
    ]

    def test_resize_url(self):
        p = Page.objects.get(pk="1")
        # check that this page has the expected jp2 filename
        self.assertEqual(p.jp2_filename, "sn83030214/00175037652/1898010101/0005.jp2")
        small = "https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2/full/200,/0/default.jpg"
        self.assertEqual(image_urls.resize_url(p, 200), small)
        large = "https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2/full/1000,/0/default.jpg"
        self.assertEqual(image_urls.resize_url(p, 1000), large)

    def test_thumb_image_url(self):
        p = Page.objects.get(pk="3")
        self.assertEqual(p.jp2_filename, "sn83030214/00175037652/1898010101/0003.jp2")
        self.assertEqual(image_urls.thumb_image_url(p), "https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0003.jp2/full/240,/0/default.jpg")
