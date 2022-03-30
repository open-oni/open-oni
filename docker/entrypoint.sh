#!/bin/bash
#
# entrypoint.sh copies the startup and management files into their proper
# locations, then fires off startup.sh

src=/opt/openoni/docker

# Set source to the read-only ONI source mount for test runs
if [[ $ONLY_RUN_TESTS == 1 ]]; then
  src=/usr/local/src/openoni/docker
fi

mkdir -p /var/local/onidata/batches
cp $src/pip-install.sh /pip-install.sh
cp $src/pip-reinstall.sh /pip-reinstall.sh
cp $src/pip-update.sh /pip-update.sh
cp $src/load_batch.sh /load_batch.sh
cp $src/_startup_lib.sh /_startup_lib.sh

cp $src/test.sh /test.sh
cp $src/manage /usr/local/bin/manage
cp $src/django-admin /usr/local/bin/django-admin

# Copy startup script based on whether this is a test-only container
if [[ $ONLY_RUN_TESTS == 1 ]]; then
  cp $src/test-startup.sh /startup.sh
else
  cp $src/startup.sh /startup.sh
fi

# Make all scripts executable
chmod u+x /*.sh
chmod u+x /usr/local/bin/*

/startup.sh
