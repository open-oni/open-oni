#!/bin/bash

# Delete Python virtual environment
rm -rf $ONI_APP_PATH/ENV

# Reinstall Python virtual environment and dependencies
/pip-install.sh

# Restart Apache
apachectl restart

