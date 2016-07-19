#!/bin/bash
source /opt/openoni/ENV/bin/activate
/opt/openoni/manage.py collectstatic --noinput
