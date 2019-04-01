################################################################
# DJANGO SETTINGS
################################################################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': 60 * 60 * 24 * 7 * 8
    }
}

DEBUG = False

# Suggested order: https://docs.djangoproject.com/en/1.10/ref/middleware/#middleware-ordering
MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'core.middleware.TooBusyMiddleware',                               # OpenONI
    'django.middleware.http.ConditionalGetMiddleware',                 # OpenONI
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',             # OpenONI
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Fingerprint compiled static files with MD5 hash of contents
# Store hashes in STATIC_ROOT directory as staticfiles.json
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'


################################################################
# OPENONI SETTINGS
################################################################
IS_PRODUCTION = True
