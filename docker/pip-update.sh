#!/bin/bash

# Activate the Python virtual environment
source ENV/bin/activate

# Update dependencies
pip install -U -r requirements.txt

# Update requirements.lock
pip freeze > requirements.lock
