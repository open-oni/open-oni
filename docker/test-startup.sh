#!/bin/bash
cp onisite/urls_example.py onisite/urls.py

export DJANGO_SETTINGS_MODULE=onisite.test_settings

source /_startup_lib.sh

verify_config
setup_database
setup_index
prep_webserver

echo "Testing"

source ENV/bin/activate
coverage run --source="." --branch \
    --omit="ENV/*,*_example.py,onisite/settings*,onisite/test_settings.py,onisite/urls.py,core/migrations/*,core/tests/*,onisite/wsgi.py" \
    manage.py test --keepdb

rm -rf static/cov
coverage html -d static/cov/
coverage report >static/cov/raw.txt
