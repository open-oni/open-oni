# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# "Private" aliases for seconds in a day and week
_ONEDAY = 60 * 60 * 24
_ONEWEEK = _ONEDAY * 7

####################################################################
# DJANGO SETTINGS
####################################################################

# If true, provides detailed logging and error pages.  DO NOT SET THIS TO TRUE
# IN PRODUCTION!
DEBUG = True

# Time zone name for django internally to use
TIME_ZONE = 'America/New_York'

# App language code: used for I18n translations
LANGUAGE_CODE = 'en-us'

# Site id differentiates DB data if multiple sites use the same database
SITE_ID = 1

# I18n and L10n settings for translating and localizing the app
USE_I18N = True
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files
# (We don't need this)
MEDIA_ROOT = ''
MEDIA_URL = ''

# Determines how we store static files; e.g., CSS, images, etc.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# Base URL to static files
STATIC_URL = '/media/'

# Directory path to static files
STATIC_ROOT = os.path.join(BASE_DIR, '.static-media')

# Module which processes URL routing
ROOT_URLCONF = 'onisite.urls'

# Database settings.  This should be overridden in settings_local.py or
# /etc/openoni.ini.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'openoni',
        'USER': 'openoni',
        'PASSWORD': 'openoni',
        }
    }

# Make this unique, and don't share it with anybody.  This MUST be overridden
# either in settings_local.py or /etc/openoni.ini.
SECRET_KEY = ''

# Classes which implement request/response middleware
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'core.middleware.TooBusyMiddleware',
)

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
            # Callables which alter the request context
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'core.context_processors.extra_request_info',
                'core.context_processors.newspaper_info',
            ],

            # Template engine debug info; Defaults to the value of DEBUG
            #'debug': True,
        },
    },
]

# List of configuration classes / app packages in order of priority (i.e., the
# first item in the list has final say when collisions occur)
INSTALLED_APPS = (
    'django.contrib.humanize',
    'django.contrib.staticfiles',

    'themes.default',
    'core',
)

# Determines how django does its caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': _ONEWEEK * 8
    }
}

# Hosts/domain names that are valid for this site.  This MUST be overridden in
# settings_local.py if you aren't in DEBUG mode.
#
# TODO: Allow this to be overridden by the INI file as well
ALLOWED_HOSTS = []

####################################################################
# 3RD-PARTY LIB SETTINGS
####################################################################


####################################################################
# OPEN-ONI SETTINGS
####################################################################

# Should be turned on in production.  TODO: this should probably drive the
# DEBUG setting, at least forcing it to be off when IS_PRODUCTION is true.  We
# should also make this overrideable in the INI file.
IS_PRODUCTION = False

LOG_LOCATION = "/opt/openoni/log/"

# Public URLs to the image server endpoints
#
# These must be overridden to point to the image server.  They may be set to
# the same value, but they're kept apart to allow for having static thumbnails,
# thumbnail caching separated from resize caching, etc.  Thumbnails are a much
# smaller subset of possible images and therefore benefit a great deal from
# being cached and/or pregenerated.
RESIZE_SERVER = "http://example.com/images/iiif"
TILE_SERVER = "http://example.com/images/iiif"

# How big should thumbnails be?
THUMBNAIL_WIDTH = 240

# These determine the life of various caches (via cache_page)
DEFAULT_TTL_SECONDS = _ONEDAY
PAGE_IMAGE_TTL_SECONDS = _ONEWEEK * 2
API_TTL_SECONDS = 60 * 60  # 1 hour
FEED_TTL_SECONDS = _ONEWEEK

# Turn this on to allow using tiff files for serving images.  Much faster than
# JP2s if you don't have Aware, but significantly more memory-intense.
USE_TIFF = False

# Set this to a server load value at which you want Open ONI to stop handling
# web requests.  If you aren't sure, just leave this alone.
TOO_BUSY_LOAD_AVERAGE = 64

# URL to the Solr server.  This should be overridden in settings_local.py or
# else /etc/openoni.ini.
SOLR = "http://localhost:8983/solr"

# Languages solr uses
SOLR_LANGUAGES = ("eng", "fre", "spa", "ger", "ita",)

# Absolute path on disk to the data directory
STORAGE = '/opt/openoni/data/'

# URL path to the data directory
STORAGE_URL = '/data/'

# If LC is down, we've mirrored a few records for development use - just copy
# the line below into settings_local.py and uncomment it:
# MARC_RETRIEVAL_URLFORMAT = "https://raw.githubusercontent.com/open-oni/marc-mirror/master/%s/marc.xml"
MARC_RETRIEVAL_URLFORMAT = "http://chroniclingamerica.loc.gov/lccn/%s/marc.xml"

# Various storage subdirectories
BATCH_STORAGE = os.path.join(STORAGE, "batches")
BIB_STORAGE = os.path.join(STORAGE, "bib")
OCR_DUMP_STORAGE = os.path.join(STORAGE, "ocr")
COORD_STORAGE = os.path.join(STORAGE, "word_coordinates")
TEMP_TEST_DATA = os.path.join(STORAGE, "temp_test_data")

# List of breadcrumbs that will be shown on all pages
BASE_CRUMBS = [{'label':'Home', 'href': '/'}]

# BASE_URL is the URL at which this site is hosted, e.g.,
# http://oregonnews.uoregon.edu.  If this isn't set in the INI file, it *must*
# be set in settings_local.py.  Leaving it at the default will not work for
# production or demoing purposes.
#
# NOTE: as of now this can NOT include any path elements!
BASE_URL = 'http://localhost'

# SITE_TITLE that will be used for display purposes throughout app
# PROJECT_NAME may be the same as SITE_TITLE but can be used
# for longer descriptions that will only show up occasionally
# Example "Open ONI" for most headers, "Open Online Newspapers Initiative"
# for introduction / about / further information / etc
# Both should be overridden in settings_local.py
SITE_TITLE = "Open ONI"
PROJECT_NAME = "Open Online Newspapers Initiative"
