#!/bin/bash
source /_startup_lib.sh

verify_config
replace_ini_data
setup_database
prep_webserver
run_apache
