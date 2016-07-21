#!/bin/bash

echo "Testing"

cd /opt/openoni
source ENV/bin/activate
coverage run --source="." --branch manage.py test --keepdb --settings=onisite.test_settings
rm -rf static/cov
coverage html -d static/cov/ --omit="ENV/*"
coverage report --omit="ENV/*,*_example.py" >static/cov/raw.txt

echo
echo "Visit $APP_URL/coverage to see a coverage report"
echo "Visit $APP_URL/coverage/raw.txt to see the raw report, including branch information"
