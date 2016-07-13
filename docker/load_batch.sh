#!/bin/bash

BATCH=$1

source /opt/openoni/ENV/bin/activate
django-admin.py load_batch /opt/openoni/data/batches/$BATCH
