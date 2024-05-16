#!/bin/bash

# Create Python virtual environment if not present
if [ ! -d /opt/openoni/ENV/lib ]; then
  python3 -m venv ENV
fi

# Activate the Python virtual environment
source ENV/bin/activate

# Bootstrap pip installer in virtual environment
# https://docs.python.org/3/library/ensurepip.html
python3 -m ensurepip

# Install Open ONI dependencies
# --no-cache-dir no longer disables building wheels in local cache,
# so install wheel package to prevent bdist_wheel errors
pip install wheel
pip install -r requirements.lock
