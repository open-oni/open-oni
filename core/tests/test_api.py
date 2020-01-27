import json

from django.test import TestCase
from django.conf import settings

class ApiTests(TestCase):
    """Tests the current API. Note URLs are hardwired instead of dynamic
    using names from urls.py to help notice when we break our contract with
    clients outside of LC.
    """

    fixtures = ['test/countries.json', 'test/titles.json',
                'test/awardee.json', 'test/batch.json', 'test/issue.json',
                'test/page.json']

    def test_newspaper_json(self):
        r = self.client.get("/newspapers.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {'@context': 'http://iiif.io/api/presentation/2/context.json',
             '@id': 'https://oni.example.com/newspapers.json',
             '@type': 'sc:Collection',
             'collections': [{'@id': 'https://oni.example.com/lccn/sn83030214.json',
                               '@type': 'sc:Collection',
                               'label': 'New-York tribune.'}],
             'label': 'Newspapers'})

    def test_title_json(self):
        r = self.client.get("/lccn/sn83030214.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {'@context': 'http://iiif.io/api/presentation/2/context.json',
             '@id': 'https://oni.example.com/lccn/sn83030214.json',
             '@type': 'sc:Collection',
             'label': 'New-York tribune.',
             'manifests': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1.json',
                             '@type': 'sc:Manifest',
                             'label': '1898-01-01'}],
             'metadata': [
                           {'label': 'id', 'value': '/lccn/sn83030214/'},
                           {'label': 'type', 'value': 'title'},
                           {'label': 'title', 'value': 'New-York tribune.'},
                           {'label': 'title normal', 'value': 'New-York tribune.'},
                           {'label': 'lccn', 'value': 'sn83030214'},
                           {'label': 'place of publication', 'value': 'New York [N.Y.]'},
                           {'label': 'frequency', 'value': 'Daily'},
                           {'label': 'publisher', 'value': 'New York Tribune'},
                           {'label': 'start year', 'value': 1866},
                           {'label': 'end year', 'value': 1924},
                           {'label': 'language', 'value': [{'@value': 'English'}]},
                           {'label': 'subject',
                            'value': [{'@value': 'New York (N.Y.)--Newspapers.'},
                                      {'@value': 'New York County (N.Y.)--Newspapers.'}]},
                           {'label': 'note',
                            'value': [{'@value': "I'll take Manhattan"},
                                      {'@value': 'The Big Apple'}]},
                           {'label': 'city',
                            'value': [{'@value': 'New York City'},
                                      {'@value': 'New York City'}]},
                           {'label': 'county', 'value': [{'@value': 'Brooklyn'}, {'@value': 'Queens'}]},
                           {'label': 'state',
                            'value': [{'@value': 'New York'}, {'@value': 'New York'}]},
                           {'label': 'place',
                            'value': [{'@value': 'New York--Brooklyn--New York City'},
                                      {'@value': 'New York--Queens--New York City'}]}]})

    def test_issue_json(self):
        r = self.client.get("/lccn/sn83030214/1898-01-01/ed-1.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {'@context': 'http://iiif.io/api/presentation/2/context.json',
             '@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1.json',
             '@type': 'sc:Manifest',
             'label': 'New-York tribune. [1898-01-01]',
             'sequences': [{'@type': 'sc:Sequence',
                             'canvases': [{'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                            '@type': 'sc:Canvas',
                                            'height': 8677,
                                            'images': [{'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                         '@type': 'oa:Annotation',
                                                         'motivation': 'sc:painting',
                                                         'on': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                         'rendering': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.pdf',
                                                                         'format': 'application/pdf'},
                                                                        {'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.jp2',
                                                                         'format': 'image/jp2'},
                                                                        {'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/',
                                                                         'format': 'text/html'}],
                                                         'resource': {'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                                       '@type': 'dctypes:Image',
                                                                       'format': 'image/jpeg',
                                                                       'height': 8677,
                                                                       'service': {'@context': 'http://iiif.io/api/image/2/context.json',
                                                                                    '@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                                                    'profile': 'http://iiif.io/api/image/2/level0.json'},
                                                                       'width': 6394},
                                                         'seeAlso': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/ocr.xml',
                                                                       'format': 'text/xml'}]}],
                                            'label': '1',
                                            'thumbnail': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2/full/240,/0/default.jpg',
                                            'width': 6394},

                                            {
                                                '@id': 'https://oni.example.com/images/iiif/None',
                                                '@type': 'sc:Canvas',
                                                'width': 4500,
                                                'height': 6825,
                                                'label': '2',
                                                'metadata': [
                                                    {'label': 'Note about reproduction', 'value': 'Not digitized, published'},
                                                ],
                                            },

											{'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0003.jp2',
											'@type': 'sc:Canvas',
											'height': 8600,
											'images': [{'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0003.jp2',
											'@type': 'oa:Annotation',
											'motivation': 'sc:painting',
											'on': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0003.jp2',
											'rendering': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-3.pdf',
											'format': 'application/pdf'},
											{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-3.jp2',
											'format': 'image/jp2'},
											{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-3/',
											'format': 'text/html'}],
											'resource': {'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0003.jp2',
											'@type': 'dctypes:Image',
											'format': 'image/jpeg',
											'height': 8600,
											'service': {'@context': 'http://iiif.io/api/image/2/context.json',
											'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0003.jp2',
											'profile': 'http://iiif.io/api/image/2/level0.json'},
											'width': 6400},
											'seeAlso': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-3/ocr.xml',
											'format': 'text/xml'}]}],
											'label': '3',
											'thumbnail': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0003.jp2/full/240,/0/default.jpg',
											'width': 6400}],
                             'label': 'issue order'}]})

    def test_page_json(self):
        r = self.client.get("/lccn/sn83030214/1898-01-01/ed-1/seq-1.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
             '@type': 'sc:Canvas',
             'height': 8677,
             'images': [{'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                          '@type': 'oa:Annotation',
                          'motivation': 'sc:painting',
                          'on': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                          'rendering': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.pdf',
                                          'format': 'application/pdf'},
                                         {'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.jp2',
                                          'format': 'image/jp2'},
                                         {'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/',
                                          'format': 'text/html'}],
                          'resource': {'@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                        '@type': 'dctypes:Image',
                                        'format': 'image/jpeg',
                                        'height': 8677,
                                        'service': {'@context': 'http://iiif.io/api/image/2/context.json',
                                                     '@id': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                     'profile': 'http://iiif.io/api/image/2/level0.json'},
                                        'width': 6394},
                          'seeAlso': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/ocr.xml',
                                        'format': 'text/xml'}]}],
             'label': '1',
             'thumbnail': 'https://oni.example.com/images/iiif/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2/full/240,/0/default.jpg',
             'width': 6394})

    def test_batch_json(self):
        r = self.client.get("/batches/batch_curiv_ahwahnee_ver01.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {'@context': 'http://iiif.io/api/presentation/2/context.json',
             '@id': 'https://oni.example.com/batches/batch_curiv_ahwahnee_ver01.json',
             '@type': 'sc:Collection',
             'label': 'batch_curiv_ahwahnee_ver01',
             'manifests': [{'@id': 'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1.json',
                             '@type': 'sc:Manifest',
                             'label': 'New-York tribune. [1898-01-01]'}],
             'metadata': [{'label': 'Ingested',
                            'value': '2009-03-27T00:59:28+00:00'},
                           {'label': 'Pages', 'value': 3},
                           {'label': 'Awardee',
                            'value': 'University of California, Riverside'}]})

    def test_awardee_json(self):
        r = self.client.get("/awardees/curiv.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {'@context': 'http://iiif.io/api/presentation/2/context.json',
             '@id': 'https://oni.example.com/awardees/curiv.json',
             '@type': 'sc:Collection',
             'collections': [{'@context': 'http://iiif.io/api/presentation/2/context.json',
                               '@id': 'https://oni.example.com/batches/batch_curiv_ahwahnee_ver01.json',
                               '@type': 'sc:Collection',
                               'label': 'batch_curiv_ahwahnee_ver01',
                               'metadata': [{'label': 'Ingested',
                                              'value': '2009-03-27T00:59:28+00:00'},
                                             {'label': 'Pages', 'value': 3},
                                             {'label': 'Awardee',
                                              'value': 'University of California, Riverside'}]}],
             'label': 'University of California, Riverside'})

    def test_batches_json(self):
        r = self.client.get("/batches.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {'@context': 'http://iiif.io/api/presentation/2/context.json',
             '@id': 'https://oni.example.com/batches.json',
             '@type': 'sc:Collection',
             'collections': [{'@context': 'http://iiif.io/api/presentation/2/context.json',
                               '@id': 'https://oni.example.com/batches/batch_curiv_ahwahnee_ver01.json',
                               '@type': 'sc:Collection',
                               'label': 'batch_curiv_ahwahnee_ver01',
                               'metadata': [{'label': 'Ingested',
                                              'value': '2009-03-27T00:59:28+00:00'},
                                             {'label': 'Pages', 'value': 3},
                                             {'label': 'Awardee',
                                              'value': 'University of California, Riverside'}]}],
             'label': 'Batches'})
