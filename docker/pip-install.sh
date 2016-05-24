#!/bin/bash

# Installs pip dependencies
cd /opt/openoni
virtualenv ENV
source ENV/bin/activate
cp conf/openoni.pth ENV/lib/python2.7/site-packages/openoni.pth
pip install -U distribute
pip install -r requirements.pip --allow-all-external

install -d /opt/openoni/static
install -d /opt/openoni/.python-eggs
