#!/bin/bash

BATCH=$1

source /opt/openoni/ENV/bin/activate

cd /opt/openoni
django-admin.py purge_batch $BATCH
