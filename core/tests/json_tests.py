from django.test import TestCase

try:
    import simplejson as json
except ImportError:
    import json

from openoni.core import models as m

class JsonTests(TestCase):
    fixtures = ['batch.json']

    def test_speedups(self):
        # simplejson needs to have c bits comiled to be fast enough
        self.assertTrue(json._speedups)

    def test_batch(self):
        b = m.Batch.objects.get(name='batch_curiv_ahwahnee_ver01')
        data = b.json(host="example.com")
        j = json.loads(data)
        self.assertEqual(j,
            {'@context': 'http://iiif.io/api/presentation/2/context.json',
             '@id': 'https://oni.example.com/batches/batch_curiv_ahwahnee_ver01.json',
             '@type': 'sc:Collection',
             'label': 'batch_curiv_ahwahnee_ver01',
             'manifests': [],
             'metadata': [{'label': 'Ingested', 'value': '2009-03-26T20:59:28-04:00'},
                          {'label': 'Pages', 'value': 0},
                          {'label': 'Awardee',
                           'value': 'University of California, Riverside; Riverside, CA'}]})
