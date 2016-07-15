#!/bin/bash

# Installs pip dependencies
virtualenv ENV
source ENV/bin/activate
pip install -U setuptools
pip install -r requirements.pip --allow-all-external

install -d /opt/openoni/static
install -d /opt/openoni/.python-eggs
