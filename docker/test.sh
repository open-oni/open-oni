#!/bin/bash

APP=${1:-core}
VERBOSITY=${2:-0}

echo "Testing $APP"

source /opt/openoni/ENV/bin/activate

cd /opt/openoni
django-admin.py test $APP --keepdb --pattern="*_tests.py" --verbosity=$VERBOSITY --settings=openoni.test_settings
