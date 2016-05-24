#!/bin/bash

APP=core

source /opt/openoni/ENV/bin/activate

cd /opt/openoni
django-admin.py test $APP