#!/bin/bash

# Create and activate Python virtual environment
virtualenv ENV
source ENV/bin/activate

# Update pip and setuptools
pip install -U pip
pip install -U setuptools

# Install / update Open ONI dependencies
pip install -U -r requirements.pip

# Miscellaneous
install -d /opt/openoni/static
install -d /opt/openoni/.python-eggs

# Update requirements.lock
pip list --format freeze > requirements.lock
