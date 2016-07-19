#!/bin/bash
source /opt/openoni/ENV/bin/activate
/opt/openoni/manage.py purge_batch $1
