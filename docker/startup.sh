#!/bin/bash

# Make sure settings_local.py exists so the app doesn't crash
if [ ! -f onisite/settings_local.py ]; then
  touch onisite/settings_local.py
fi
# Make sure we have a default urls.py
if [ ! -f onisite/urls.py ]; then
  cp onisite/urls_example.py onisite/urls.py
fi

# Die on missing APP_URL; this one could default to localhost, except that the
# RAIS container won't have gotten it set, making it incapable of reporting the
# IIIF URLs to images
if [[ ${APP_URL:-} == "" ]]; then
  echo
  echo
  echo "Cannot start ONI: you must set \$APP_URL in your environment.  e.g.:"
  echo
  echo "    export APP_URL=http://oregonnews.uoregon.edu"
  echo "    docker-compose up"
  echo
  echo
  exit 1
fi

export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
mkdir -p /var/tmp/django_cache && chown -R www-data:www-data /var/tmp/django_cache
mkdir -p /opt/openoni/log

if [ ! -d /opt/openoni/ENV ]; then
  /pip-install.sh
fi

# Generate a random secret key if that hasn't already happened.  This stays the
# same after it's first set.
sed -i "s/!SECRET_KEY!/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 80)/g" /etc/openoni.ini.orig

# Refresh the environmental config for APP_URL in case it needs to change
cp /etc/openoni.ini.orig /etc/openoni.ini
sed -i "s|!APP_URL!|$APP_URL|g" /etc/openoni.ini

# Hack apache to do the RAIS proxying
cp /etc/apache2/sites-available/openoni-orig.conf /etc/apache2/sites-available/openoni.conf
sed -i "s/!RAIS_HOST!/rais/g" /etc/apache2/sites-available/openoni.conf
a2ensite openoni

cd /opt/openoni
source ENV/bin/activate

DB_READY=0
MAX_TRIES=15
TRIES=0
while [ $DB_READY == 0 ]
  do
   if
     ! mysql -uroot -hrdbms -p123456 \
       -e 'ALTER DATABASE openoni charset=utf8'
   then
     sleep 5
     let TRIES++
     echo "Looks like we're still waiting for RDBMS ... 5 more seconds ... retry $TRIES of $MAX_TRIES"
     if [ "$TRIES" = "$MAX_TRIES" ]
     then
      echo "Looks like we couldn't get RDBMS running. Could you check settings and try again?"
      echo "ERROR: The database was not setup properly."
      exit 2
     fi
   else
     DB_READY=1
   fi
done

echo "setting up a test database ..."
mysql -uroot -hrdbms -p123456 \
  -e 'USE mysql; GRANT ALL on test_openoni.* TO "openoni"@"%" IDENTIFIED BY "openoni";'

echo "-------" >&2
echo "Migrating database" >&2
/opt/openoni/manage.py migrate

echo "-------" >&2
echo "Running collectstatic" >&2
/opt/openoni/manage.py collectstatic --noinput

# Remove any pre-existing PID file which prevents Apache from starting
#   thus causing the container to close immediately after
#   See: https://github.com/docker-library/php/pull/59
rm -f /var/run/apache2/apache2.pid

echo "ONI setup successful; starting Apache"
source /etc/apache2/envvars
exec apache2 -D FOREGROUND
