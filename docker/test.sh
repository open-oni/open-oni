#!/bin/bash

echo "Testing"

cd /opt/openoni
source ENV/bin/activate
coverage run --source="." manage.py test --keepdb --settings=onisite.test_settings
rm -rf static/cov
coverage html -d static/cov/ --omit="ENV/*"
