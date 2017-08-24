#!/bin/bash
source /_startup_lib.sh

verify_config
verify_vars
replace_ini_data
setup_database
prep_webserver

echo "Testing"

cd /opt/openoni
source ENV/bin/activate
coverage run --source="." --branch \
    --omit="ENV/*,*_example.py,onisite/settings*,onisite/test_settings.py,onisite/urls.py,core/migrations/*,core/tests/*,onisite/wsgi.py" \
    manage.py test --keepdb --settings=onisite.test_settings
rm -rf static/cov
coverage html -d static/cov/
coverage report >static/cov/raw.txt

echo
cat static/cov/raw.txt
