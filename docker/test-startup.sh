#!/bin/bash
# Create a copy of ONI code with more carefully constructed settings and urls
# for testing without pulling in custom plugins or themes
rsync -avq \
  --exclude="data/*" \
  --exclude="static/cov/*" \
  --exclude="onisite/plugins/*" \
  --exclude="themes/*" \
  --exclude="log/*" \
  --exclude="ENV/*" \
  /usr/local/src/openoni/ /opt/openoni
cd /opt/openoni
rsync -avq /usr/local/src/openoni/themes/default/ /opt/openoni/themes/default
cp /usr/local/src/openoni/themes/__init__.py /opt/openoni/themes/__init__.py
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
