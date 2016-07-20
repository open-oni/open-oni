#!/bin/bash
source /opt/openoni/ENV/bin/activate
/opt/openoni/manage.py load_batch /opt/openoni/data/batches/$1
