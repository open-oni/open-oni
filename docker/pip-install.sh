#!/bin/bash

# Create and activate Python virtual environment
pip3 install -U pip
pip install -U setuptools
pip install -U virtualenv
virtualenv -p python3 ENV
source ENV/bin/activate

# Install Open ONI dependencies
pip install -r requirements.lock
