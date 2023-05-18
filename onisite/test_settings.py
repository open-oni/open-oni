from .settings_base import *

# Required settings that don't really matter, but need to exist for tests to run
LOG_LOCATION = BASE_DIR / 'log'
PROJECT_NAME = 'Open Online Newspapers Initiative'
SECRET_KEY = "FOO"
SITE_TITLE = 'Open ONI'
SOLR_BASE_URL = 'http://solr:8983'
STORAGE_URL = '/data/'
TITLE_DISPLAY_MEDIUM = False
TOO_BUSY_LOAD_AVERAGE = 64

# Storage path and dependent settings
STORAGE = BASE_DIR / 'data'
BATCH_STORAGE = STORAGE / 'batches'
COORD_STORAGE = STORAGE / 'word_coordinates'
OCR_DUMP_STORAGE = STORAGE / 'ocr'
TEMP_TEST_DATA = STORAGE / 'temp_test_data'

# These are explicitly overridden in order to verify the JSON is using the
# proper URLs, and not "http://testserver"
BASE_URL = "https://oni.example.com"
IIIF_URL = BASE_URL + "/images/iiif"

# List of configuration classes / app packages in order of priority (i.e., the
# first item in the list has final say when collisions occur)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.staticfiles',
    'themes.default',
    'core',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.DisableClientSideCachingMiddleware',             # Open ONI
    'core.middleware.TooBusyMiddleware',                              # Open ONI
    'django.middleware.http.ConditionalGetMiddleware',                # Open ONI
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Reset back to Django defaults to keep test output simple
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

del LOGGING
