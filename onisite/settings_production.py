################################################################
# DJANGO SETTINGS
################################################################
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
        'TIMEOUT': _ONEWEEK * 8
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
    'django.middleware.csrf.CsrfViewMiddleware',
#    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Use cache with storing static files; e.g., CSS, images, etc.
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'


################################################################
# OPENONI SETTINGS
################################################################
IS_PRODUCTION = True
