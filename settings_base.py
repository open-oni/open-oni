import os

# Local variable for making fairly decent assumptions
DIRNAME = os.path.abspath(os.path.dirname(__file__))

# If true, provides detailed logging and error pages.  DO NOT SET THIS TO TRUE
# IN PRODUCTION!
DEBUG = True

# DEPRECATED as of Django 1.8!
#
# If TRUE *and* DEBUG is true, provides detailed information when template
# rendering causes exceptions.
TEMPLATE_DEBUG = DEBUG

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

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

STATIC_URL = '/media/'
STATIC_ROOT = os.path.join(DIRNAME, '.static-media')

ROOT_URLCONF = 'openoni.urls'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'openoni',
        'USER': 'openoni',
        'PASSWORD': 'openoni',
        }
    }

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'openoni.core.middleware.TooBusyMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'openoni.core.context_processors.extra_request_info',
    'openoni.core.context_processors.newspaper_info',
)

TEMPLATE_DIRS = (
    os.path.join(DIRNAME, 'templates'),
)

INSTALLED_APPS = (
    # 'lc',
    # 'openoni.example',
    # 'openoni.loc',
    'south',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'djcelery',
    'djkombu',

    'openoni.core',
)

BROKER_TRANSPORT = "django"

THUMBNAIL_WIDTH = 360

DEFAULT_TTL_SECONDS = 86400  # 1 day
PAGE_IMAGE_TTL_SECONDS = 60 * 60 * 24 * 7 * 2  # 2 weeks
API_TTL_SECONDS = 60 * 60  # 1 hour
FEED_TTL_SECONDS = 60 * 60 * 24 * 7

USE_TIFF = False

SOUTH_TESTS_MIGRATE = False
ESSAYS_FEED = "http://ndnp-essays.rdc.lctl.gov/feed/"

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 4838400,  # 2 months
    }
}

IS_PRODUCTION = False
CTS_USERNAME = 'username'
CTS_PASSWORD = 'password'
CTS_PROJECT_ID = 'ndnp'
CTS_QUEUE = 'ndnpingestqueue'
CTS_SERVICE_TYPE = 'ingest.NdnpIngest.ingest'
CTS_URL = "https://cts.loc.gov/transfer/"

MAX_BATCHES = 0

import multiprocessing
#TOO_BUSY_LOAD_AVERAGE = 1.5 * multiprocessing.cpu_count()
TOO_BUSY_LOAD_AVERAGE = 64 

SOLR = "http://localhost:8983/solr"
SOLR_LANGUAGES = ("eng", "fre", "spa", "ger", "ita",)

DOCUMENT_ROOT = "/opt/openoni/static"

STORAGE = '/opt/openoni/data/'
STORAGE_URL = '/data/'
BATCH_STORAGE = os.path.join(STORAGE, "batches")
BIB_STORAGE = os.path.join(STORAGE, "bib")
OCR_DUMP_STORAGE = os.path.join(STORAGE, "ocr")
COORD_STORAGE = os.path.join(STORAGE, "word_coordinates")
TEMP_TEST_DATA = os.path.join(STORAGE, "temp_test_data")


BASE_CRUMBS = [{'label':'Home', 'href': '/'}]

TOPICS_ROOT_URL = 'http://www.loc.gov/rr/news/topics'
TOPICS_SUBJECT_URL = '/topicsSubject.html'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']
