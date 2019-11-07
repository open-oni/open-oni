from settings_base import *

# Required settings that don't really matter, but need to exist for tests to run
SECRET_KEY = "FOO"
LOG_LOCATION = '/opt/openoni/log/'
OCR_DUMP_STORAGE = '/tmp/ocr'
SITE_TITLE = 'Open ONI'
PROJECT_NAME = 'Open Online Newspapers Initiative'
STORAGE = '/opt/openoni/data/'
BATCH_STORAGE = os.path.join(STORAGE, 'batches')
COORD_STORAGE = os.path.join(STORAGE, 'word_coordinates')
OCR_DUMP_STORAGE = os.path.join(STORAGE, 'ocr')
TEMP_TEST_DATA = os.path.join(STORAGE, 'temp_test_data')
STORAGE_URL = '/data/'
TITLE_DISPLAY_MEDIUM = False
TOO_BUSY_LOAD_AVERAGE = 64
IS_PRODUCTION = False
SOLR = 'http://solr:8983/solr/openoni'

# These are explicitly overridden in order to verify the JSON is using the
# proper URLs, and not "http://testserver"
BASE_URL="https://oni.example.com"
RESIZE_SERVER = BASE_URL+"/images/resize"
TILE_SERVER = BASE_URL+"/images/tile"

# List of configuration classes / app packages in order of priority (i.e., the
# first item in the list has final say when collisions occur)
INSTALLED_APPS = (
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
