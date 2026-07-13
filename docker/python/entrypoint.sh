#!/bin/bash

# We symlink configs from /var/local/oni-config so that volume can be exposed
# for direct configuration editing *without* exposing things that could
# accidentally break ONI
confdir="/var/local/oni-config"
onisite="/opt/openoni/onisite"

for prefix in settings_local urls; do
  file="$prefix.py"
  ex="${prefix}_example.py"
  if [ ! -f $confdir/$file ]; then
    echo "Copying defaults for $file"
    cp $onisite/$ex $confdir/$file
  fi

  # This is sort of overkill / brute-force, but ensures we *always* rely on
  # /var/local/oni-config and never allow a non-linked file for settings.
  rm -f $onisite/$file
  ln -s $confdir/$file $onisite/$file
done

# These are semi-fast, and critical to run. On first start we need them run,
# obviously, but also after importing data, restoring a backup, etc.
echo "Initializing databases"
/opt/openoni/manage.py migrate
/opt/openoni/manage.py setup_index

# We run collectstatic only when the "compiled" subdir doesn't exist *and* the
# directory is mounted read-write (in case we share parts of the entrypoint,
# split up gunicorn from a management-only service, etc). This one is slow
# enough at times that it's better to make people run it manually if they need
# a one-off run.
if [ ! -d /opt/openoni/static/compiled ] && [ -w /opt/openoni/static ]; then
  echo "Compiling static assets"
  /opt/openoni/manage.py collectstatic --noinput
fi

echo "Executing \"$@\"..."
exec "$@"
