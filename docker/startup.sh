#!/bin/bash
source /_startup_lib.sh

verify_config
setup_database
setup_index
prep_webserver
run_apache
