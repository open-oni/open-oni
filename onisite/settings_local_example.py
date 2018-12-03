import os

################################################################
# ENVIRONMENT INDEPENDENT SETTINGS
################################################################
# Use only if LoC is down and MARC requests fail
# We've mirrored a *lot* of MARC records on GitHub
# MARC_RETRIEVAL_URLFORMAT = 'https://raw.githubusercontent.com/open-oni/marc-mirror/master/marc/%s/marc.xml'
# To serve locally, clone open-oni/marc-mirror repository
# to static/compiled/marc and use below
# MARC files may be updated periodically with getlc.go Go script
#MARC_RETRIEVAL_URLFORMAT = 'http://YOUR_HOSTNAME/static/marc/%s/marc.xml'



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
    'themes.default',
    'core',
)



################################################################
# PRODUCTION ENVIRONMENT
# To use, comment all dev env settings above and uncomment below
# Replace all "YOUR_*" strings below with appropriate values
################################################################
#from settings_production import *

  ################################################################
  # DJANGO SETTINGS
  ################################################################
#ALLOWED_HOSTS = ['YOUR_HOSTNAME']

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'HOST': 'rdbms',
#        'NAME': 'openoni',
#        'USER': 'openoni',
#        'PASSWORD': 'YOUR_DB_PASSWORD',
#    }
#}

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

  ################################################################
  # OPENONI SETTINGS
  ################################################################
# BASE_URL is the URL at which this site is hosted
# NOTE: as of now this can NOT include any path elements!
#BASE_URL = 'http://YOUR_HOSTNAME'

#LOG_LOCATION = '/opt/openoni/log/'

# Enable HSTS by setting SECURE_HSTS_SECONDS > 0
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
# Test with a low value (e.g. 300)
# before setting a high value (e.g. 15552000) for long-term use
#SECURE_HSTS_SECONDS = 0

# SITE_TITLE that will be used for display purposes throughout app
# PROJECT_NAME may be the same as SITE_TITLE but can be used
# for longer descriptions that will only show up occasionally
# Example 'Open ONI' for most headers, 'Open Online Newspapers Initiative'
# for introduction / about / further information / etc
#SITE_TITLE = 'YOUR_SHORT_PROJECT_NAME'
#PROJECT_NAME = 'YOUR_LONG_PROJECT_NAME'

# Absolute path on disk to the data directory
#STORAGE = '/opt/openoni/data/'
    # Various storage subdirectories
#BATCH_STORAGE = os.path.join(STORAGE, 'batches')
#COORD_STORAGE = os.path.join(STORAGE, 'word_coordinates')
#OCR_DUMP_STORAGE = os.path.join(STORAGE, 'ocr')
#TEMP_TEST_DATA = os.path.join(STORAGE, 'temp_test_data')

# URL path to the data directory
#STORAGE_URL = '/data/'

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
#RESIZE_SERVER = 'http://YOUR_HOSTNAME/images/iiif'
#TILE_SERVER = 'http://YOUR_HOSTNAME/images/iiif'


  ################################################################
  # SOLR SETTINGS
  ################################################################
# URL to the Solr server
#SOLR = 'http://YOUR_HOSTNAME:8983/solr'

