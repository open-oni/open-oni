import os

from .django_defaults import *

################################################################
# DJANGO CUSTOMIZATIONS
################################################################
# https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
# Maintain past default setting to avoid extra migrations
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Our URLs are within the onisite app
ROOT_URLCONF = 'onisite.urls'

# Enable browser XSS protection, MIME-type sniff prevention headers,
# and disable framing / embedding
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Site id differentiates DB data if multiple sites use the same database
SITE_ID = 1

# Directory path to static files
#STATIC_ROOT = os.path.join(BASE_DIR, 'static', 'compiled')
STATIC_ROOT = BASE_DIR / 'static' / 'compiled'

# Template configuration (1.8+)
TEMPLATES = [
    {
        # Whether engine looks inside application directories for templates
        'APP_DIRS': True,

        # Template engine
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Template-containing directories
        'DIRS': [
#            os.path.join(BASE_DIR, 'templates'),
            BASE_DIR / 'templates',
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

                # Open ONI
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

# Our application is within the onisite app
WSGI_APPLICATION = 'onisite.wsgi.application'


################################################################
# DEFAULT OPEN-ONI SETTINGS
################################################################
# These determine the life of various caches (via cache_page)
API_TTL_SECONDS = 60 * 60  # One hour
DEFAULT_TTL_SECONDS = API_TTL_SECONDS * 24  # One day
FEED_TTL_SECONDS = DEFAULT_TTL_SECONDS * 7  # One week
PAGE_IMAGE_TTL_SECONDS = FEED_TTL_SECONDS * 2  # Two weeks

# List of breadcrumbs that will be shown on all pages
BASE_CRUMBS = [{'label':'Home', 'href': '/'}]

# Relative path from core and theme apps to subdirectory with essay templates.
# For example: 'essays' will find files in themes/*/templates/essays
ESSAY_TEMPLATES = 'essays'

# Batch, title management, log directory path
#LOG_LOCATION = os.path.join(BASE_DIR, 'log', '')
LOG_LOCATION = BASE_DIR / 'log'

MARC_RETRIEVAL_URLFORMAT = 'https://chroniclingamerica.loc.gov/lccn/%s/marc.xml'

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny'
    ]
}

# Display newspaper titles with medium ("volume", "microform") when available
TITLE_DISPLAY_MEDIUM = False


################################################################
# DEFAULT IIIF SETTINGS
################################################################
# How big should thumbnails be?
THUMBNAIL_WIDTH = 240

# Use JP2 file paths with RAIS rather than TIFF file paths
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


################################################################
# ENVIRONMENT SETTINGS
################################################################
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.mysql',
        'HOST':     os.getenv('ONI_DB_HOST', 'rdbms'),
        'PORT':     os.getenv('ONI_DB_PORT', 3306),
        'NAME':     os.getenv('ONI_DB_NAME', 'openoni'),
        'USER':     os.getenv('ONI_DB_USER', 'openoni'),
        'PASSWORD': os.getenv('ONI_DB_PASSWORD', 'openoni'),
        'OPTIONS': { 'init_command': "SET sql_mode='STRICT_TRANS_TABLES'" },
    }
}

DEBUG = True if os.getenv('ONI_DEBUG', 0) == '1' else False

## Log level: start with INFO level; change to DEBUG if insufficient
LOG_LEVEL = os.getenv('ONI_LOG_LEVEL', 'INFO')

# Set up default logging configuration; this sets up various optional handlers,
# only enabling the console output by default
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_true': {'()': 'django.utils.log.RequireDebugTrue'},
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} [{levelname}] {module} {process:d} {thread:d} - {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'class': 'logging.FileHandler',
#            'filename': os.path.join(LOG_LOCATION, 'debug.log'),
            'filename': LOG_LOCATION / 'debug.log',
            'formatter': 'verbose',
        },
        'sql': {
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
        }
    },
    'loggers': {},
    'root': {
        'handlers': ['console'],
        'level': LOG_LEVEL,
    },
}

"""
Django logging outputs in Apache logs by default.
Log to file when Apache logs don't provide info or tracebacks.
Ensure file is writeable by Apache user with SELinux writeable context:
    chcon -t httpd_sys_rw_content_t /path/to/debug.log
"""
if os.getenv('ONI_LOG_TO_FILE', 0) == '1':
    LOGGING['root']['handlers'].append('file')

# If ONI_LOG_SQL is true, the SQL-logging handler is enabled.  This requires
# DEBUG to be true, otherwise logs will still be suppressed.
if os.getenv('ONI_LOG_SQL', 0) == '1':
    LOGGING['loggers']['django.db.backends'] = {
        'level': 'DEBUG',
        'handlers': ['sql'],
    }

SECRET_KEY = os.getenv('ONI_SECRET_KEY', 'openoni')

SOLR_BASE_URL = os.getenv('ONI_SOLR_URL', 'http://solr:8983')

## Absolute path on disk to the data directory
#STORAGE = os.getenv('ONI_STORAGE_PATH', os.path.join(BASE_DIR, 'data'))
STORAGE = os.getenv('ONI_STORAGE_PATH', BASE_DIR / 'data')


#################################################################
## DEBUG / PRODUCTION MODE
#################################################################
if DEBUG:
    """
    DEBUG mode (not production) disables Django cache, sends emails to console,
    and adds middleware that disables all client-side caching.
    """
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache'
        }
    }

    # Output emails to console
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Suggested order: https://docs.djangoproject.com/en/3.2/ref/middleware/#middleware-ordering
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

    # Suggested order: https://docs.djangoproject.com/en/3.2/ref/middleware/#middleware-ordering
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
