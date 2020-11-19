#!/bin/bash

# Create Python virtual environment if not present
if [ ! -d /opt/openoni/ENV/lib ]; then
  python3 -m venv ENV
fi

# Activate the Python virtual environment
source ENV/bin/activate

# Install Open ONI dependencies
# --no-cache-dir disables building local wheels as packages are installed
# Building wheels provides no benefit when isolated within virtual environment
pip install --no-cache-dir -r requirements.lock
