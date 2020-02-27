#!/bin/bash

# Create and activate Python virtual environment
pip3 install -U pip
pip install -U setuptools
pip install -U virtualenv
virtualenv -p python3 ENV
source ENV/bin/activate

# Install / update Open ONI dependencies
pip install -U -r requirements.pip

# Miscellaneous
install -d /opt/openoni/static
install -d /opt/openoni/.python-eggs

# Update requirements.lock
pip list --format freeze > requirements.lock
