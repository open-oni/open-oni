import os
import urlparse

# For initial customization, search and update values beginning with 'YOUR_'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

################################################################
# ENVIRONMENT SETTINGS
################################################################
# BASE_URL can NOT include any path elements!
BASE_URL = os.getenv('ONI_BASE_URL', 'http://localhost')
    # BASE_URL-dependent Settings
url = urlparse.urlparse(BASE_URL)

ALLOWED_HOSTS = [url.netloc]

# HTTPS Settings
if url.scheme == 'https':
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    """
    Enable HSTS by setting SECURE_HSTS_SECONDS > 0.
    Test with a low value (e.g. 300)
    before setting a high value (e.g. 15552000) for long-term use
    """
    SECURE_HSTS_SECONDS = os.getenv('ONI_HSTS_SECONDS', 0)
    SECURE_SSL_REDIRECT = True if SECURE_HSTS_SECONDS > 0 else False
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True if SECURE_HSTS_SECONDS > 0 else False
    SECURE_HSTS_PRELOAD = True if SECURE_HSTS_SECONDS > 0 else False

# IIIF server public URL endpoints
RESIZE_SERVER = BASE_URL + '/images/resize'
TILE_SERVER = BASE_URL + '/images/iiif'
    # End of BASE_URL-dependent Settings

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'HOST':     os.getenv('ONI_DB_HOST', 'rdbms'),
        'PORT':     os.getenv('ONI_DB_PORT', 3306),
        'NAME':     os.getenv('ONI_DB_NAME', 'openoni'),
        'USER':     os.getenv('ONI_DB_USER', 'openoni'),
        'PASSWORD': os.getenv('ONI_DB_PASSWORD', 'openoni'),
    }
}

DEBUG = True if os.getenv('ONI_DEBUG', 0) == '1' else False

SECRET_KEY = os.getenv('ONI_SECRET_KEY', 'openoni')

SOLR = os.getenv('ONI_SOLR_URL', 'http://solr:8983/solr/openoni')

# Absolute path on disk to the data directory
STORAGE = os.getenv('ONI_STORAGE_PATH', os.path.join(BASE_DIR, 'data'))
    # STORAGE-dependent Settings
BATCH_STORAGE = os.path.join(STORAGE, 'batches')
COORD_STORAGE = os.path.join(STORAGE, 'word_coordinates')
OCR_DUMP_STORAGE = os.path.join(STORAGE, 'ocr')
TEMP_TEST_DATA = os.path.join(STORAGE, 'temp_test_data')
    # End of STORAGE-dependent Settings

"""
Django logging outputs in Apache logs by default.
Log to file when Apache logs don't provide info or tracebacks.
Ensure file is writeable by Apache user with SELinux writeable context:
    chcon -t httpd_sys_rw_content_t /path/to/debug.log
Start with INFO level; change to DEBUG if insufficient
"""
if os.getenv('ONI_LOG_TO_FILE', 0) == '1':
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': os.path.join(BASE_DIR, 'log', 'debug.log'),
            },
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'INFO',
                'propagate': True,
            },
        },
    }


################################################################
# DJANGO SETTINGS
################################################################
# Keep database connections open until idle for this many seconds
CONN_MAX_AGE = 30

# List of configuration classes / app packages in order of priority high to low.
# The first item in the list has final say when collisions occur.
INSTALLED_APPS = (
    # Default
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Humanize and local theme override all below
    'django.contrib.humanize',  # Makes data more human-readable
#    'themes.YOUR_THEME_NAME',

    # Plugins
    # See https://github.com/open-oni?q=plugin for available plugins

    # Open ONI
    'sass_processor',
    'themes.default',
    'core',
)

"""
'From' address on general emails sent by Django:
If sending email from different server, replace `@' + url.netloc` with host.
Space at the end of EMAIL_SUBJECT_PREFIX intentional
to separate subject from prefix.
"""
DEFAULT_FROM_EMAIL = 'YOUR_PROJECT_NAME_ABBREVIATION-no-reply@' + url.netloc
EMAIL_SUBJECT_PREFIX = '[YOUR_PROJECT_NAME_ABBREVIATION] '


################################################################
# OPEN-ONI SETTINGS
################################################################
"""
SITE_TITLE that will be used for display purposes throughout app.
PROJECT_NAME may be the same as SITE_TITLE but can be used for longer
descriptions that will only show up occasionally.
For example: 'Open ONI' for most headers, 'Open Online Newspapers Initiative'
for introduction / about / further information / etc
"""
SITE_TITLE = 'YOUR_SHORT_PROJECT_NAME'
PROJECT_NAME = 'YOUR_LONG_PROJECT_NAME'

# Relative path from core and theme apps to subdirectory with essay templates.
# For example: 'essays' will find files in themes/*/templates/essays
ESSAY_TEMPLATES = 'essays'

"""
Use below only if LoC is down and MARC requests fail.
We've mirrored a *lot* of MARC records on GitHub for use with
"""
#MARC_RETRIEVAL_URLFORMAT = 'https://raw.githubusercontent.com/open-oni/marc-mirror/master/marc/%s/marc.xml'
"""
To serve locally, clone open-oni/marc-mirror repository
to static/compiled/marc and use setting below.
MARC files may be updated periodically with getlc.go Go script.
"""
#MARC_RETRIEVAL_URLFORMAT = BASE_URL + '/static/marc/%s/marc.xml'

"""
Number of processes in system run queue averaged over last minute beyond which
Open ONI will return a 'Server Too Busy' response. If unsure, leave at default.
Requires core.middleware.TooBusyMiddleware in MIDDLEWARE.
"""
TOO_BUSY_LOAD_AVERAGE = 64


if DEBUG:
    """
    DEBUG mode (not production) disables Django cache, sends emails to console,
    and adds middleware that disables all client-side caching.
    SQL logging is optional in DEBUG mode with env var ONI_LOG_SQL.
    Note that SQL logging will override logging to a file with ONI_LOG_TO_FILE.
    """
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }
    }

    # Output emails to console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Suggested order: https://docs.djangoproject.com/en/1.11/ref/middleware/#middleware-ordering
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'core.middleware.DisableClientSideCachingMiddleware',         # Open ONI
        'core.middleware.TooBusyMiddleware',                          # Open ONI
        'django.middleware.http.ConditionalGetMiddleware',            # Open ONI
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    if os.getenv('ONI_LOG_SQL', 0) == '1':
        LOGGING = {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'require_debug_true': {
                    '()': 'django.utils.log.RequireDebugTrue',
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'filters': ['require_debug_true'],
                    'class': 'logging.StreamHandler',
                }
            },
            'loggers': {
                'django.db.backends': {
                    'level': 'DEBUG',
                    'handlers': ['console'],
                }
            }
        }


else:
    """
    Production mode (DEBUG is off) uses filesystem cache, adds middleware for
    optional error reporting emails, and fingerprints static files
    """
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
            'TIMEOUT': 60 * 60 * 24 * 7 * 8  # Eight weeks
        }
    }

    # Suggested order: https://docs.djangoproject.com/en/1.11/ref/middleware/#middleware-ordering
    MIDDLEWARE = (
        'django.middleware.security.SecurityMiddleware',
        'core.middleware.TooBusyMiddleware',                          # Open ONI
        'django.middleware.http.ConditionalGetMiddleware',            # Open ONI
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    # Fingerprint compiled static files with MD5 hash of contents
    # Store hashes in STATIC_ROOT directory as staticfiles.json
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

