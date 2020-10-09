#!/bin/bash

# Create Python virtual environment if not present
if [ ! -d /opt/openoni/ENV/lib ]; then
  pip3 install -U pip
  pip install -U setuptools
  pip install -U virtualenv
  virtualenv -p python3 ENV
fi

# Activate the Python virtual environment
source ENV/bin/activate

# Install Open ONI dependencies
pip install -r requirements.lock
