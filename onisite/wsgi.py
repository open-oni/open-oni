"""
WSGI config for openoni project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/opt/openoni')
os.environ.setdefault("CELERY_LOADER", "django")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onisite.settings")

application = get_wsgi_application()
