import json

from django.test import TestCase


class ApiIiifTests(TestCase):
    """
    IIIF API. Note URLs are hardwired instead of dynamic using names
    from urls.py to help notice breaking backward-compatibility
    """

    fixtures = [
      'test/awardee.json',
      'test/batch.json',
      'test/countries.json',
      'test/issue.json',
      'test/page.json',
      'test/reel.json',
      'test/titles.json'
    ]

    def test_newspaper_json(self):
        r = self.client.get('/newspapers.json')
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
        r = self.client.get('/lccn/sn83030214.json')
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
        r = self.client.get('/lccn/sn83030214/1898-01-01/ed-1.json')
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
        r = self.client.get('/lccn/sn83030214/1898-01-01/ed-1/seq-1.json')
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
        r = self.client.get('/batches/batch_curiv_ahwahnee_ver01.json')
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
        r = self.client.get('/awardees/curiv.json')
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
        r = self.client.get('/batches.json')
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


class ApiChronamTests(TestCase):
    """
    ChronAm JSON API. Note URLs are hardwired instead of dynamic using names
    from urls.py to help notice breaking backward-compatibility
    """

    fixtures = [
        'api-chronam/awardee.json',
        'api-chronam/batch.json',
        'api-chronam/issue.json',
        'api-chronam/page.json',
        'api-chronam/titles.json',
    ]

    def test_awardee_json(self):
        r = self.client.get('/api/chronam/awardees/curiv.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(j['name'], 'University of California, Riverside')
        self.assertTrue(j['url'].endswith('/awardees/curiv.json'))
        self.assertTrue(j['batches'][0]['url'].endswith('/batches/batch_curiv_ahwahnee_ver01.json'))
        self.assertEqual(j['batches'][0]['name'], 'batch_curiv_ahwahnee_ver01')

    def test_awardee_list_json(self):
        r = self.client.get('/api/chronam/awardees.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(len(j['awardees']), 47)
        self.assertEqual(j['awardees'][0]['name'], 'Alaska State Library Historical Collections')
        self.assertIs(j['awardees'][0]['url'].endswith('/awardees/ak.json'), True)
        self.assertEqual(j['awardees'][46]['name'], 'West Virginia University')
        self.assertIs(j['awardees'][46]['url'].endswith('/awardees/wvu.json'), True)

    def test_batch_json(self):
        r = self.client.get('/api/chronam/batches/batch_does_not_exist.json')
        self.assertEqual(r.status_code, 404)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Batch does not exist')

        r = self.client.get('/api/chronam/batches/batch_curiv_ahwahnee_ver01.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(j['name'], 'batch_curiv_ahwahnee_ver01')
        self.assertEqual(j['page_count'], 1)
        self.assertEqual(j['awardee']['name'], 'University of California, Riverside')
        self.assertTrue(j['awardee']['url'].endswith('/awardees/curiv.json'))
        self.assertEqual(j['lccns'], ['sn83030214'])
        self.assertTrue(j['ingested'].startswith('2009-03-26T20:59:28'))
        self.assertEqual(j['issues'][0]['date_issued'], '1898-01-01')
        self.assertTrue(j['issues'][0]['url'].endswith('/lccn/sn83030214/1898-01-01/ed-1.json'))
        self.assertEqual(j['issues'][0]['title']['name'], 'New-York tribune.')
        self.assertTrue(j['issues'][0]['title']['url'].endswith('/lccn/sn83030214.json'))

    def test_batch_list_json(self):
        r = self.client.get('/api/chronam/batches/3.json')
        self.assertEqual(r.status_code, 400)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'That page contains no results')

        r = self.client.get('/api/chronam/batches/2.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(len(j['batches']), 1)
        self.assertEqual(j['count'], 26)
        self.assertEqual(j['pages'], 2)
        self.assertIs('next' in j, False)
        self.assertEqual(j['previous'], 'https://oni.example.com/api/chronam/batches/1.json')

        r = self.client.get('/api/chronam/batches.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(len(j['batches']), 25)
        self.assertEqual(j['count'], 26)
        self.assertEqual(j['pages'], 2)
        self.assertEqual(j['next'], 'https://oni.example.com/api/chronam/batches/2.json')
        self.assertIs('previous' in j, False)
        b = j['batches'][0]
        self.assertEqual(b['name'], 'batch_curiv_ahwahnee_ver01')
        self.assertTrue(b['url'].endswith('/batches/batch_curiv_ahwahnee_ver01.json'))
        self.assertEqual(b['page_count'], 1)
        self.assertEqual(b['lccns'], ['sn83030214'])
        self.assertEqual(b['awardee']['name'], 'University of California, Riverside')
        self.assertTrue(b['awardee']['url'].endswith('/awardees/curiv.json'))
        self.assertTrue(b['ingested'].startswith('2009-03-26T20:59:28'))

    def test_drf_http_verb_control(self):
        r = self.client.delete('/api/chronam/batches.json')
        self.assertEqual(r.status_code, 405)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Method "DELETE" not allowed.')

        r = self.client.head('/api/chronam/batches.json')
        self.assertEqual(r.status_code, 405)

        r = self.client.options('/api/chronam/batches.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(j['description'], 'api/chronam/batches.json\nList all batches')
        self.assertEqual(j['name'], 'Batch List')

        r = self.client.post('/api/chronam/batches.json')
        self.assertEqual(r.status_code, 405)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Method "POST" not allowed.')

        r = self.client.put('/api/chronam/batches.json')
        self.assertEqual(r.status_code, 405)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Method "PUT" not allowed.')

        r = self.client.trace('/api/chronam/batches.json')
        self.assertEqual(r.status_code, 405)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Method "TRACE" not allowed.')

    def test_issue_json(self):
        r = self.client.get('/api/chronam/lccn/sn83030214/0000-01-01/ed-1.json')
        self.assertEqual(r.status_code, 400)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'year 0 is out of range')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-13-01/ed-1.json')
        self.assertEqual(r.status_code, 400)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'month must be in 1..12')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-01-41/ed-1.json')
        self.assertEqual(r.status_code, 400)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'day is out of range for month')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-01-01/ed-2.json')
        self.assertEqual(r.status_code, 404)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Issue does not exist')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-01-01/ed-1.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertTrue(j['url'].endswith('/lccn/sn83030214/1898-01-01/ed-1.json'))
        self.assertTrue(j['title']['url'].endswith('/lccn/sn83030214.json'))
        self.assertEqual(j['title']['name'], 'New-York tribune.')
        self.assertEqual(j['date_issued'], '1898-01-01')
        self.assertEqual(j['volume'], '83')
        self.assertEqual(j['number'], '32')
        self.assertEqual(j['edition'], 1)
        self.assertEqual(j['pages'][0]['sequence'], 1)
        self.assertTrue(j['pages'][0]['url'].endswith('/lccn/sn83030214/1898-01-01/ed-1/seq-1.json'))

    def test_newspaper_json(self):
        r = self.client.get('/api/chronam/newspapers.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(len(j['newspapers']), 1)
        self.assertEqual(j['newspapers'][0]['lccn'], 'sn83030214')
        self.assertEqual(j['newspapers'][0]['state'], 'New York')
        self.assertEqual(j['newspapers'][0]['title'], 'New-York tribune.')
        self.assertTrue(j['newspapers'][0]['url'].endswith('/lccn/sn83030214.json'))

    def test_page_json(self):
        r = self.client.get('/api/chronam/lccn/sn83030214/0000-01-01/ed-1/seq-1.json')
        self.assertEqual(r.status_code, 400)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'year 0 is out of range')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-13-01/ed-1/seq-1.json')
        self.assertEqual(r.status_code, 400)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'month must be in 1..12')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-01-41/ed-1/seq-1.json')
        self.assertEqual(r.status_code, 400)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'day is out of range for month')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-01-01/ed-1/seq-2.json')
        self.assertEqual(r.status_code, 404)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Page does not exist')

        r = self.client.get('/api/chronam/lccn/sn83030214/1898-01-01/ed-1/seq-1.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertTrue(j['jp2'].endswith('/lccn/sn83030214/1898-01-01/ed-1/seq-1.jp2'))
        self.assertTrue(j['ocr'].endswith('/lccn/sn83030214/1898-01-01/ed-1/seq-1/ocr.xml'))
        self.assertTrue(j['pdf'].endswith('/lccn/sn83030214/1898-01-01/ed-1/seq-1.pdf'))
        self.assertTrue(j['text'].endswith('/lccn/sn83030214/1898-01-01/ed-1/seq-1/ocr.txt'))
        self.assertEqual(j['sequence'], 1)
        self.assertEqual(j['title']['name'], 'New-York tribune.')
        self.assertTrue(j['title']['url'].endswith('/lccn/sn83030214.json'))
        self.assertTrue(j['issue']['date_issued'], '1898-01-01')
        self.assertTrue(j['issue']['url'].endswith('/lccn/sn83030214/1898-01-01/ed-1.json'))

    def test_title_json(self):
        r = self.client.get('/api/chronam/lccn/does_not_exist.json')
        self.assertEqual(r.status_code, 404)
        j = json.loads(r.content)
        self.assertEqual(j['detail'], 'Title does not exist')

        r = self.client.get('/api/chronam/lccn/sn83030214.json')
        self.assertEqual(r.status_code, 200)
        j = json.loads(r.content)
        self.assertEqual(j['place_of_publication'], 'New York [N.Y.]')
        self.assertEqual(j['lccn'], 'sn83030214')
        self.assertEqual(j['start_year'], '1866')
        self.assertEqual(j['place'][0], 'New York--Brooklyn--New York City')
        self.assertEqual(j['name'], 'New-York tribune.')
        self.assertTrue(j['url'].endswith('/lccn/sn83030214.json'))
        self.assertEqual(j['subject'][0], 'New York (N.Y.)--Newspapers.')
        self.assertEqual(j['issues'][0]['date_issued'], '1898-01-01')
