#!/bin/bash

# Activate the Python virtual environment
source ENV/bin/activate

# Update dependencies
pip install -U -r requirements.pip

# Update requirements.lock
pip freeze > requirements.lock
