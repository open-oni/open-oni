from django.apps import AppConfig
from django.conf import settings as s

class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Open ONI Core'

    def ready(self):
        # Define internal settings derived from local settings
        s.SOLR = s.SOLR_BASE_URL + '/solr/openoni'

        return
