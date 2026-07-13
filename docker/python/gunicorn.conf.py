import os

wsgi_app = 'onisite.wsgi:application'
bind = "0.0.0.0:8000"
workers = int(os.environ.get("GUNICORN_WORKERS", 4))
max_requests = int(os.environ.get("GUNICORN_MAX_REQUESTS", 10000))
