#!/bin/bash

APP=${1:-core}
VERBOSITY=${2:-0}

echo "Testing $APP"

source /opt/openoni/ENV/bin/activate
/opt/openoni/manage.py test $APP --keepdb --verbosity=$VERBOSITY --settings=onisite.test_settings
