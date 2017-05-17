#!/bin/bash
#
# entrypoint.sh copies the startup and management files into their proper
# locations, then fires off startup.sh

cp /opt/openoni/docker/pip-install.sh /pip-install.sh
cp /opt/openoni/docker/load_batch.sh /load_batch.sh
cp /opt/openoni/docker/startup.sh /startup.sh
cp /opt/openoni/docker/test.sh /test.sh
cp /opt/openoni/docker/manage /usr/local/bin/manage
cp /opt/openoni/docker/django-admin /usr/local/bin/django-admin
cp /opt/openoni/docker/openoni.ini /etc/openoni.ini.orig

# Make all scripts executable
chmod u+x /*.sh
chmod u+x /usr/local/bin/*

/startup.sh
