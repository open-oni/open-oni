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
            {u'@context': u'http://iiif.io/api/presentation/2/context.json',
             u'@id': u'https://oni.example.com/newspapers.json',
             u'@type': u'sc:Collection',
             u'collections': [{u'@id': u'https://oni.example.com/lccn/sn83030214.json',
                               u'@type': u'sc:Collection',
                               u'label': u'New-York tribune.'}],
             u'label': u'Newspapers'})

    def test_title_json(self):
        r = self.client.get("/lccn/sn83030214.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {u'@context': u'http://iiif.io/api/presentation/2/context.json',
             u'@id': u'https://oni.example.com/lccn/sn83030214.json',
             u'@type': u'sc:Collection',
             u'label': u'New-York tribune.',
             u'manifests': [{u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1.json',
                             u'@type': u'sc:Manifest',
                             u'label': u'1898-01-01'}],
             u'metadata': [{u'label': u'county',
                            u'value': [{u'@value': u'Brooklyn'}, {u'@value': u'Queens'}]},
                           {u'label': u'frequency', u'value': u'Daily'},
                           {u'label': u'id', u'value': u'/lccn/sn83030214/'},
                           {u'label': u'subject',
                            u'value': [{u'@value': u'New York (N.Y.)--Newspapers.'},
                                       {u'@value': u'New York County (N.Y.)--Newspapers.'}]},
                           {u'label': u'city',
                            u'value': [{u'@value': u'New York City'},
                                       {u'@value': u'New York City'}]},
                           {u'label': u'title', u'value': u'New-York tribune.'},
                           {u'label': u'end year', u'value': 1924},
                           {u'label': u'note',
                            u'value': [{u'@value': u"I'll take Manhattan"},
                                       {u'@value': u'The Big Apple'}]},
                           {u'label': u'state',
                            u'value': [{u'@value': u'New York'},
                                       {u'@value': u'New York'}]},
                           {u'label': u'type', u'value': u'title'},
                           {u'label': u'place of publication',
                            u'value': u'New York [N.Y.]'},
                           {u'label': u'start year', u'value': 1866},
                           {u'label': u'publisher', u'value': u'New York Tribune'},
                           {u'label': u'language', u'value': [{u'@value': u'English'}]},
                           {u'label': u'lccn', u'value': u'sn83030214'},
                           {u'label': u'title normal', u'value': u'New-York tribune.'},
                           {u'label': u'place',
                            u'value': [{u'@value': u'New York--Brooklyn--New York City'},
                                       {u'@value': u'New York--Queens--New York City'}]}]})

    def test_issue_json(self):
        r = self.client.get("/lccn/sn83030214/1898-01-01/ed-1.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {u'@context': u'http://iiif.io/api/presentation/2/context.json',
             u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1.json',
             u'@type': u'sc:Manifest',
             u'label': u'New-York tribune. [1898-01-01]',
             u'sequences': [{u'@type': u'sc:Sequence',
                             u'canvases': [{u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                            u'@type': u'sc:Canvas',
                                            u'height': 8677,
                                            u'images': [{u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                         u'@type': u'oa:Annotation',
                                                         u'motivation': u'sc:painting',
                                                         u'on': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                         u'rendering': [{u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.pdf',
                                                                         u'format': u'application/pdf'},
                                                                        {u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.jp2',
                                                                         u'format': u'image/jp2'},
                                                                        {u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/',
                                                                         u'format': u'text/html'}],
                                                         u'resource': {u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                                       u'@type': u'dctypes:Image',
                                                                       u'format': u'image/jpeg',
                                                                       u'height': 8677,
                                                                       u'service': {u'@context': u'http://iiif.io/api/image/2/context.json',
                                                                                    u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                                                    u'profile': u'http://iiif.io/api/image/2/level0.json'},
                                                                       u'width': 6394},
                                                         u'seeAlso': [{u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/ocr.xml',
                                                                       u'format': u'text/xml'}]}],
                                            u'label': u'1',
                                            u'thumbnail': u'https://oni.example.com/images/resize/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2/full/240,/0/default.jpg',
                                            u'width': 6394}],
                             u'label': u'issue order'}]})

    def test_page_json(self):
        r = self.client.get("/lccn/sn83030214/1898-01-01/ed-1/seq-1.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
             u'@type': u'sc:Canvas',
             u'height': 8677,
             u'images': [{u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                          u'@type': u'oa:Annotation',
                          u'motivation': u'sc:painting',
                          u'on': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                          u'rendering': [{u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.pdf',
                                          u'format': u'application/pdf'},
                                         {u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1.jp2',
                                          u'format': u'image/jp2'},
                                         {u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/',
                                          u'format': u'text/html'}],
                          u'resource': {u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                        u'@type': u'dctypes:Image',
                                        u'format': u'image/jpeg',
                                        u'height': 8677,
                                        u'service': {u'@context': u'http://iiif.io/api/image/2/context.json',
                                                     u'@id': u'https://oni.example.com/images/tile/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2',
                                                     u'profile': u'http://iiif.io/api/image/2/level0.json'},
                                        u'width': 6394},
                          u'seeAlso': [{u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1/seq-1/ocr.xml',
                                        u'format': u'text/xml'}]}],
             u'label': u'1',
             u'thumbnail': u'https://oni.example.com/images/resize/batch_curiv_ahwahnee_ver01%2Fdata%2Fsn83030214%2F00175037652%2F1898010101%2F0005.jp2/full/240,/0/default.jpg',
             u'width': 6394})

    def test_batch_json(self):
        r = self.client.get("/batches/batch_curiv_ahwahnee_ver01.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {u'@context': u'http://iiif.io/api/presentation/2/context.json',
             u'@id': u'https://oni.example.com/batches/batch_curiv_ahwahnee_ver01.json',
             u'@type': u'sc:Collection',
             u'label': u'batch_curiv_ahwahnee_ver01',
             u'manifests': [{u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1.json',
                             u'@type': u'sc:Manifest',
                             u'label': u'New-York tribune. [1898-01-01]'}],
             u'metadata': [{u'label': u'Ingested',
                            u'value': u'2009-03-27T00:59:28+00:00'},
                           {u'label': u'Pages', u'value': 1},
                           {u'label': u'Awardee',
                            u'value': u'University of California, Riverside'}]})

    def test_awardee_json(self):
        r = self.client.get("/awardees/curiv.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {u'@context': u'http://iiif.io/api/presentation/2/context.json',
             u'@id': u'https://oni.example.com/awardees/curiv.json',
             u'@type': u'sc:Collection',
             u'collections': [{u'@context': u'http://iiif.io/api/presentation/2/context.json',
                               u'@id': u'https://oni.example.com/batches/batch_curiv_ahwahnee_ver01.json',
                               u'@type': u'sc:Collection',
                               u'label': u'batch_curiv_ahwahnee_ver01',
                               u'manifests': [{u'@id': u'https://oni.example.com/lccn/sn83030214/1898-01-01/ed-1.json',
                                               u'@type': u'sc:Manifest',
                                               u'label': u'New-York tribune. [1898-01-01]'}],
                               u'metadata': [{u'label': u'Ingested',
                                              u'value': u'2009-03-27T00:59:28+00:00'},
                                             {u'label': u'Pages', u'value': 1},
                                             {u'label': u'Awardee',
                                              u'value': u'University of California, Riverside'}]}],
             u'label': u'University of California, Riverside'})

    def test_batches_json(self):
        r = self.client.get("/batches.json")
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.maxDiff = None
        self.assertEqual(j,
            {u'@context': u'http://iiif.io/api/presentation/2/context.json',
             u'@id': u'https://oni.example.com/batches.json',
             u'@type': u'sc:Collection',
             u'collections': [{u'@context': u'http://iiif.io/api/presentation/2/context.json',
                               u'@id': u'https://oni.example.com/batches/batch_curiv_ahwahnee_ver01.json',
                               u'@type': u'sc:Collection',
                               u'label': u'batch_curiv_ahwahnee_ver01',
                               u'metadata': [{u'label': u'Ingested',
                                              u'value': u'2009-03-27T00:59:28+00:00'},
                                             {u'label': u'Pages', u'value': 1},
                                             {u'label': u'Awardee',
                                              u'value': u'University of California, Riverside'}]}],
             u'label': u'Batches'})
