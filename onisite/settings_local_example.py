import os

################################################################
# ENVIRONMENT INDEPENDENT SETTINGS
################################################################
# From address on general emails sent by Django
# If sending email from same server as Django, end with @YOUR_WEB_HOST
#DEFAULT_FROM_EMAIL = 'YOUR_PROJECT_NAME_ABBREVIATION-no-reply@YOUR_EMAIL_HOST'
#EMAIL_SUBJECT_PREFIX = '[YOUR_PROJECT_NAME_ABBREVIATION] '

# Django logging outputs in Apache logs by default
# Log to file when Apache logs don't provide info or tracebacks
# Ensure file is writeable by Apache user
# With SELinux set writeable context: chcon -t httpd_sys_rw_content_t file_path
# Start with INFO level; change to DEBUG if insufficient
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'handlers': {
#        'file': {
#            'level': 'INFO',
#            'class': 'logging.FileHandler',
#            'filename': 'YOUR_LOG_PATH/debug.log',
#        },
#    },
#    'loggers': {
#        'django': {
#            'handlers': ['file'],
#            'level': 'INFO',
#            'propagate': True,
#        },
#    },
#}

# Use only if LoC is down and MARC requests fail
# We've mirrored a *lot* of MARC records on GitHub
# MARC_RETRIEVAL_URLFORMAT = 'https://raw.githubusercontent.com/open-oni/marc-mirror/master/marc/%s/marc.xml'
# To serve locally, clone open-oni/marc-mirror repository
# to static/compiled/marc and use below
# MARC files may be updated periodically with getlc.go Go script
#MARC_RETRIEVAL_URLFORMAT = 'http://YOUR_WEB_HOST/static/marc/%s/marc.xml'



################################################################
# DEVELOPMENT ENVIRONMENT
################################################################
from settings_development import *

# List of configuration classes / app packages in order of priority (i.e., the
# first item in the list has final say when collisions occur)
INSTALLED_APPS = (
    # Default
#    'django.contrib.admin',
#    'django.contrib.auth',
#    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Plugins
    # See https://github.com/open-oni?q=plugin for available plugins

    # OpenONI
    'django.contrib.humanize',  # Added to make data more human-readable
    'sass_processor',
    'themes.default',
    'core',
)

# Uncomment to enable SQL query output in Django logging
#LOGGING = {
#    'version': 1,
#    'disable_existing_loggers': False,
#    'filters': {
#        'require_debug_true': {
#            '()': 'django.utils.log.RequireDebugTrue',
#        }
#    },
#    'handlers': {
#        'console': {
#            'level': 'DEBUG',
#            'filters': ['require_debug_true'],
#            'class': 'logging.StreamHandler',
#        }
#    },
#    'loggers': {
#        'django.db.backends': {
#            'level': 'DEBUG',
#            'handlers': ['console'],
#        }
#    }
#}



################################################################
# PRODUCTION ENVIRONMENT
# To use, comment all dev env settings above and uncomment below
# Replace all "YOUR_*" strings below with appropriate values
################################################################
#from settings_production import *

  ################################################################
  # DJANGO SETTINGS
  ################################################################
#ALLOWED_HOSTS = ['YOUR_WEB_HOST']

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'HOST': 'YOUR_DB_HOST',
#        'NAME': 'openoni',
#        'USER': 'openoni',
#        'PASSWORD': 'YOUR_DB_PASSWORD',
#    }
#}
#CONN_MAX_AGE = 30

# EMAIL_HOST settings only necessary if another server or service sends emails
# Defaults to 'localhost', sending from the same server running Django
# Additional settings for further email host configuration:
# https://docs.djangoproject.com/en/1.11/ref/settings/#email-host
#EMAIL_HOST = 'YOUR_EMAIL_HOST'
#EMAIL_HOST_PASSWORD = 'YOUR_EMAIL_HOST_PASSWORD'
#EMAIL_HOST_USER = 'YOUR_EMAIL_HOST_USER'
    # ADMINS receive 5xx error emails; MANAGERS receive 404 error emails
# From address on error emails sent to ADMINS and MANAGERS
# If sending email from same server as Django, end with @YOUR_WEB_HOST
#SERVER_EMAIL = 'YOUR_PROJECT_NAME_ABBREVIATION-no-reply@YOUR_EMAIL_HOST'
#ADMINS = [
#    ('YOUR_admin1', 'YOUR_admin1@example.com'),
#    ('YOUR_adminX', 'YOUR_adminX@example.com')
#]
#MANAGERS = [
#    ('YOUR_mngr1', 'YOUR_mngr13@example.com'),
#    ('YOUR_mngrX', 'YOUR_mngrX4@example.com')
#]
#IGNORABLE_404_URLS = [
#    re.compile(r'YOUR_known_404_URL_regex_to_prevent_emails'),
#]

# List of configuration classes / app packages in order of priority (i.e., the
# first item in the list has final say when collisions occur)
#INSTALLED_APPS = (
#    # Default
##    'django.contrib.admin',
##    'django.contrib.auth',
##    'django.contrib.contenttypes',
#    'django.contrib.sessions',
#    'django.contrib.messages',
#    'django.contrib.staticfiles',
#
#    # Plugins
#    # See https://github.com/open-oni?q=plugin for available plugins
#
#    # OpenONI
#    'django.contrib.humanize',  # Added to make data more human-readable
#    'themes.YOUR_THEME_NAME',
#    'themes.default',
#    'core',
#)

#SECRET_KEY = 'YOUR_SECRET_KEY'

# HTTPS Settings
#CSRF_COOKIE_SECURE = True
#SESSION_COOKIE_SECURE = True
# Enable HSTS by setting SECURE_HSTS_SECONDS > 0
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
# Test with a low value (e.g. 300)
# before setting a high value (e.g. 15552000) for long-term use
#SECURE_HSTS_SECONDS = 0
#SECURE_SSL_REDIRECT = True


  ################################################################
  # OPENONI SETTINGS
  ################################################################
# BASE_URL is the URL at which this site is hosted
# NOTE: as of now this can NOT include any path elements!
#BASE_URL = 'http://YOUR_WEB_HOST'

# Relative path from core and theme apps to subdirectory where essay templates are stored
# example: "essays" would find files in themes/default/templates/essays
#ESSAY_TEMPLATES = "essays"

# Batch and title management log directory path
#LOG_LOCATION = 'YOUR_LOG_PATH'

# SITE_TITLE that will be used for display purposes throughout app
# PROJECT_NAME may be the same as SITE_TITLE but can be used
# for longer descriptions that will only show up occasionally
# Example 'Open ONI' for most headers, 'Open Online Newspapers Initiative'
# for introduction / about / further information / etc
#SITE_TITLE = 'YOUR_SHORT_PROJECT_NAME'
#PROJECT_NAME = 'YOUR_LONG_PROJECT_NAME'

# Absolute path on disk to the data directory
# If STORAGE is set here, subdirectories must be as well
#STORAGE = 'YOUR_DATA_PATH'
    # Various storage subdirectories
#BATCH_STORAGE = os.path.join(STORAGE, 'batches')
#COORD_STORAGE = os.path.join(STORAGE, 'word_coordinates')
#OCR_DUMP_STORAGE = os.path.join(STORAGE, 'ocr')
#TEMP_TEST_DATA = os.path.join(STORAGE, 'temp_test_data')

# URL path to the data directory
#STORAGE_URL = '/data/'

# Displays newspaper titles with medium ("volume", "microform") when available
#TITLE_DISPLAY_MEDIUM = False

# Number of processes in system run queue averaged over last minute beyond which
# OpenONI will return a 'Server Too Busy' response; If unsure, leave at default
# Requires core.middleware.TooBusyMiddleware in MIDDLEWARE
#TOO_BUSY_LOAD_AVERAGE = 64


  ################################################################
  # IIIF SETTINGS
  ################################################################
# Public URLs to the image server endpoints
# They may be set to the same value, but they're kept apart to allow for having
# static thumbnails, thumbnail caching separated from resize caching, etc.
# Thumbnails are a much smaller subset of possible images and therefore benefit
# a great deal from being cached and/or pregenerated.
#RESIZE_SERVER = 'http://YOUR_WEB_HOST/images/resize'
#TILE_SERVER = 'http://YOUR_WEB_HOST/images/iiif'


  ################################################################
  # SOLR SETTINGS
  ################################################################
# URL to the Solr server
#SOLR = 'http://YOUR_SOLR_HOST:8983/solr'

