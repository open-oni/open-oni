#!/bin/bash

BATCH=$1

source /opt/openoni/ENV/bin/activate
django-admin.py purge_batch $BATCH
