#!/bin/bash

source ENV/bin/activate

# Update dependencies
pip install -U -r requirements.pip

# Update requirements.lock
pip list --format freeze > requirements.lock
