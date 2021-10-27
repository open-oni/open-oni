import glob
import logging
import os
import requests
import time
from urllib import parse

from django.core.management.base import BaseCommand
from django.conf import settings
from core.management.commands import configure_logging

configure_logging('setup_index_logging.config', 'setup_index.log')


_logger = logging.getLogger(__name__)
fixture_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../fixtures'))
if settings.SOLR_CLOUD:
    core_url = settings.SOLR_BASE_URL + '/api/collections/openoni?action=STATUS&indexInfo=true'
    schema_url = settings.SOLR_BASE_URL + '/api/collections/openoni/schema'
else:
    core_url = settings.SOLR_BASE_URL + '/api/cores/openoni?action=STATUS&indexInfo=true'
    schema_url = settings.SOLR_BASE_URL + '/api/cores/openoni/schema'


# Copy fields are defined here because we have to manually check for dupes; for
# some reason Solr doesn't do this for us, and will in fact allow dozens of the
# same copy-field definition.  The structure should be obvious, and is the
# exact format Solr's API takes.
copy_fields = [
    {'source': 'place_of_publication', 'dest': 'place_of_publication_facet'},
    {'source': 'subject', 'dest': 'subject_facet'},
    {'source': 'title', 'dest': 'title_facet'},
    {'source': 'ocr_*', 'dest': '_text_'}
]

class Command(BaseCommand):
    help = 'Set up all Solr index configuration necessary for Open ONI'

    def handle(self, **options):
        _logger.info('Loading Solr schema fixtures')

        # Wait for SOLR to respond and report that the openoni core is there
        if not self.wait_for_solr():
            _logger.error('Exiting...')
            return

        # Schema fixtures must be idempotent!  Nothing here should cause
        # problems if run multiple times.
        schema_fixtures = sorted(glob.glob(os.path.join(fixture_dir, 'solr-schema', '*.json')))
        for fixture in schema_fixtures:
            if not self.load_schema_fixture(fixture):
                _logger.error('Exiting...')
                return

        _logger.info('Adding copy fields')
        existing_copy_fields = self.get_existing_copy_fields()
        for definition in copy_fields:
            if not self.defined_copy_field(existing_copy_fields, definition):
                if not self.create_copy_field(definition):
                    _logger.error('Exiting...')
                    return

    def wait_for_solr(self):
        for x in range(0, 120):
            if x != 0:
                time.sleep(1)
            if x % 5 == 0:
                _logger.info('Checking Solr connectivity')

            try:
                with requests.get(core_url, timeout=1.0) as r:
                    if r.status_code != 200:
                        if x % 5 == 0:
                            _logger.info('Solr is not ready; waiting...')
                        continue



                    if settings.SOLR_CLOUD:
                      if len(r.json().get('cluster', {}).get('live_nodes', [])) > 0:
                        return True
                    else:
                      status = r.json().get('status', {}).get('openoni', {})
                      if 'uptime' in status:
                          return True

                    if x % 5 == 0:
                        _logger.info('Solr is initializing the openoni core; waiting...')
                    continue

            except requests.exceptions.RequestException:
                if x % 5 == 0:
                    _logger.info('Solr is not responding; waiting...')
                continue

        _logger.error(f'Solr is not ready after {x} seconds; aborting')
        return False

    def get_existing_copy_fields(self):
        with requests.get(schema_url) as r:
            if r.status_code != 200:
                _logger.error('Unable to read schema from Solr: ' + r.text)
                _logger.error('Exiting...')
                return

            schema = r.json()['schema']
            if 'copyFields' in schema:
                return schema['copyFields']

    def defined_copy_field(self, existing_copy_fields, definition):
        for existing_definition in existing_copy_fields:
            if definition == existing_definition:
                return True
        return False

    def create_copy_field(self, definition):
        json = {'add-copy-field': definition}
        with requests.post(schema_url, json=json) as r:
            if r.status_code != 200:
                _logger.error(f'Error adding {definition}: {r.text}')
                return False
        return True

    def load_schema_fixture(self, fname):
        _logger.info('- ' + fname)
        with open(fname, 'rb') as f:
            with requests.post(schema_url, data=f) as r:
                if not self.valid_response(r):
                    errmsg = r.json()['error']['msg']
                    _logger.error(f'Error loading fixture file {fname}: {errmsg}')
                    return False

        return True

    def valid_response(self, r):
        if r.status_code == 200:
            return True

        # A 400 can indicate things which aren't actually errors, like fields
        # already existing.  All other codes, however, are considered failures.
        if r.status_code != 400:
            return False

        # We run through all errors instead of stopping at the first so we can
        # clearly see every problem instead of fixing one, rerunning, fixing
        # the next, etc.
        success = True
        for detail in r.json()['error']['details']:
            if 'add-field-type' in detail:
                if not self.valid_add_field_type_response(detail):
                    success = False
            elif 'add-field' in detail:
                if not self.valid_add_field_response(detail):
                    success = False
            # Flag anything unknown as an invalid response just to be safe
            else:
                _logger.error('Error: ' + r.text)
                success = False

        return success

    def valid_add_field_type_response(self, detail):
        info = detail['add-field-type']
        name = info['name']
        errors = detail['errorMessages']
        if len(errors) == 1 and errors[0] == f"Field type '{name}' already exists.\n":
            return True

        _logger.error(f"Unable to add field type '{name}': " + ', '.join(errors))
        return False

    def valid_add_field_response(self, detail):
        info = detail['add-field']
        name = info['name']
        errors = detail['errorMessages']
        if len(errors) == 1 and errors[0] == f"Field '{name}' already exists.\n":
            return True

        _logger.error(f"Unable to add field '{name}': " + ', '.join(errors))
        return False

