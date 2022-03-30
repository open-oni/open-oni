"""
ASGI config for openoni project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
import sys

from django.core.asgi import get_asgi_application

sys.path.append('/opt/openoni')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onisite.settings')

application = get_asgi_application()
