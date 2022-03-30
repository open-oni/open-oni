#!/bin/bash

# Create Python virtual environment if not present
if [ ! -d /opt/openoni/ENV/lib ]; then
  python3 -m venv ENV
fi

# Activate the Python virtual environment
source ENV/bin/activate

# Install Open ONI dependencies
# --no-cache-dir no longer disables building wheels in local cache,
# so install wheel package to prevent bdist_wheel errors
pip install wheel
pip install -r requirements.lock
