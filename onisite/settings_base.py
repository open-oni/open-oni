import os

from django_defaults import *

################################################################
# PRIVATE CONSTANTS
################################################################
# 'Private' aliases for seconds in a day and week
_ONEDAY = 60 * 60 * 24
_ONEWEEK = _ONEDAY * 7


################################################################
# DJANGO CUSTOMIZATIONS
################################################################
# Enable browser XSS protection, MIME-type sniff prevention headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Site id differentiates DB data if multiple sites use the same database
SITE_ID = 1

# Directory path to static files
STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'compiled')

# Template configuration (1.8+)
TEMPLATES = [
    {
        # Whether engine looks inside application directories for templates
        'APP_DIRS': True,

        # Template engine
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Template-containing directories
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],

        'OPTIONS': {
            # https://docs.djangoproject.com/en/1.9/topics/templates/#module-django.template.backends.django
            
            # Callables which alter the request context
            'context_processors': [
                # Default
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
#                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # OpenONI
                'django.template.context_processors.csrf',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'core.context_processors.extra_request_info',
            ],
        },
    },
]


################################################################
# DEFAULT OPEN-ONI SETTINGS
################################################################
# These determine the life of various caches (via cache_page)
API_TTL_SECONDS = 60 * 60  # 1 hour
DEFAULT_TTL_SECONDS = _ONEDAY
FEED_TTL_SECONDS = _ONEWEEK
PAGE_IMAGE_TTL_SECONDS = _ONEWEEK * 2

# List of breadcrumbs that will be shown on all pages
BASE_CRUMBS = [{'label':'Home', 'href': '/'}]

MARC_RETRIEVAL_URLFORMAT = 'https://chroniclingamerica.loc.gov/lccn/%s/marc.xml'


################################################################
# DEFAULT IIIF SETTINGS
################################################################
# How big should thumbnails be?
THUMBNAIL_WIDTH = 240

# Turn this on to allow using tiff files for serving images.  Much faster than
# JP2s if you don't have Aware, but significantly more memory-intense.
USE_TIFF = False


################################################################
# DEFAULT SOLR SETTINGS
################################################################
# Languages solr uses
SOLR_LANGUAGES = (
    'ara',
    'arm',
    'baq',
    'bul',
    'cze',
    'dan',
    'dut',
    'eng',
    'fin',
    'fre',
    'ger',
    'gle',
    'gre',
    'hin',
    'hun',
    'ind',
    'ita',
    'jpn',
    'lav',
    'nor',
    'per',
    'por',
    'rum',
    'rus',
    'spa',
    'swe',
    'tha',
    'tur',
)

