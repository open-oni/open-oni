#!/bin/bash

echo "Testing"

cd /opt/openoni
source ENV/bin/activate
coverage run --source="." --branch \
    --omit="ENV/*,*_example.py,onisite/settings*,onisite/test_settings.py,onisite/urls.py,core/migrations/*,core/tests/*,onisite/wsgi.py" \
    manage.py test --settings=onisite.test_settings
rm -rf static/cov
coverage html -d static/cov/
coverage report >static/cov/raw.txt

echo
echo "Visit $APP_URL/coverage to see a coverage report"
echo "Visit $APP_URL/coverage/raw.txt to see the raw text report"
