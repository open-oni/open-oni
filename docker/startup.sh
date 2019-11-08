#!/bin/bash
source /_startup_lib.sh

verify_config
setup_database
prep_webserver
run_apache
