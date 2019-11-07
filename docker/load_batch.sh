#!/bin/bash
source $ONI_APP_PATH/ENV/bin/activate
$ONI_APP_PATH/manage.py load_batch $ONI_APP_PATH/data/batches/$1
