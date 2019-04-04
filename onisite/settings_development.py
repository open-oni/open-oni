import os

################################################################
# DJANGO SETTINGS
################################################################
ALLOWED_HOSTS = ['*']

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
    }
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'rdbms',
        'NAME': 'openoni',
        'USER': 'openoni',
        'PASSWORD': 'openoni',
    }
}

DEBUG = True

# Output emails to console for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Suggested order: https://docs.djangoproject.com/en/1.10/ref/middleware/#middleware-ordering
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.DisableClientSideCachingMiddleware',              # OpenONI
    'core.middleware.TooBusyMiddleware',                               # OpenONI
    'django.middleware.http.ConditionalGetMiddleware',                 # OpenONI
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


################################################################
# OPENONI SETTINGS
################################################################
# BASE_URL is the URL at which this site is hosted
# NOTE: as of now this can NOT include any path elements!
BASE_URL = 'http://localhost'

# Relative path from core and theme apps to subdirectory where essay templates are stored
# example: "essays" would find files in themes/default/templates/essays
ESSAY_TEMPLATES = "essays"

IS_PRODUCTION = False

LOG_LOCATION = '/opt/openoni/log/'

# Public URLs to the image server endpoints
# They may be set to the same value, but they're kept apart to allow for having
# static thumbnails, thumbnail caching separated from resize caching, etc.
# Thumbnails are a much smaller subset of possible images and therefore benefit
# a great deal from being cached and/or pregenerated.
RESIZE_SERVER = 'http://localhost/images/iiif'
TILE_SERVER = 'http://localhost/images/iiif'

# SITE_TITLE that will be used for display purposes throughout app
# PROJECT_NAME may be the same as SITE_TITLE but can be used
# for longer descriptions that will only show up occasionally
# Example 'Open ONI' for most headers, 'Open Online Newspapers Initiative'
# for introduction / about / further information / etc
SITE_TITLE = 'Open ONI'
PROJECT_NAME = 'Open Online Newspapers Initiative'

# Absolute path on disk to the data directory
STORAGE = '/opt/openoni/data/'
    # Various storage subdirectories
BATCH_STORAGE = os.path.join(STORAGE, 'batches')
COORD_STORAGE = os.path.join(STORAGE, 'word_coordinates')
OCR_DUMP_STORAGE = os.path.join(STORAGE, 'ocr')
TEMP_TEST_DATA = os.path.join(STORAGE, 'temp_test_data')

# URL path to the data directory
STORAGE_URL = '/data/'

# Displays newspaper titles with medium ("volume", "microform") when available
TITLE_DISPLAY_MEDIUM = False

# Number of processes in system run queue averaged over last minute beyond which
# OpenONI will return a 'Server Too Busy' response; If unsure, leave at default
# Requires core.middleware.TooBusyMiddleware in MIDDLEWARE_CLASSES
TOO_BUSY_LOAD_AVERAGE = 64


################################################################
# SOLR SETTINGS
################################################################
# URL to the Solr server
SOLR = 'http://solr:8983/solr/openoni'

