from os.path import dirname, join

from django.test import TestCase

from core.ocr_extractor import ocr_extractor


class OcrExtractorTests(TestCase):

    def test_extractor(self):
        dir = join(dirname(dirname(__file__)), 'test-data')
        ocr_file = join(dir, 'ocr.xml')
        text, coord_info = ocr_extractor(ocr_file)
        coords = coord_info["coords"]
        expected_text = {"eng": open(join(dir, 'ocr.txt'), encoding='utf-8').read()}

        self.assertEqual(text, expected_text)
        self.assertEqual(len(list(coords.keys())), 2150)
        self.assertEqual(len(coords['place']), 3)
        # Craft. should be normalized to Craft
        # since Solr's highlighting will not include
        # trailing punctuation in highlighted text
        self.assertTrue('Craft' in coords)
        self.assertTrue('Craft.' not in coords)
