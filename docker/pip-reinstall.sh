#!/bin/bash

# Delete Python virtual environment
rm -rf /opt/openoni/ENV

# Reinstall Python virtual environment and dependencies
/pip-install.sh

# Restart Apache
apachectl restart

