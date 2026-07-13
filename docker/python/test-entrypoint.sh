#!/bin/bash

echo "Initializing databases"
/opt/openoni/manage.py migrate
/opt/openoni/manage.py setup_index

echo "Executing \"$@\"..."
exec "$@"
