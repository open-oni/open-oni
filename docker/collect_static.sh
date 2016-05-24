#!/bin/bash

source /opt/openoni/ENV/bin/activate

cd /opt/openoni
django-admin.py collectstatic --noinput
