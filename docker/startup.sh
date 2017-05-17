#!/bin/bash
urlfile="/opt/openoni/onisite/urls.py"
if [ ! -f $urlfile ]; then
  echo
  echo
  echo "Cannot start ONI: you must create onisite/urls.py, e.g.:"
  echo
  echo "    cp onisite/urls_example.py onisite/urls.py"
  echo "    docker-compose up"
  echo
  echo "(You may wish to edit your local URL rules, but the defaults will work for a simple setup)"
  echo
  exit 1
fi

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

# Refresh the environmental config for DB and Solr hosts in case of IP changes
cp /etc/openoni.ini.orig /etc/openoni.ini

sed -i "s/!DB_HOST!/rdbms/g" /etc/openoni.ini
sed -i "s/!SOLR_HOST!/solr/g" /etc/openoni.ini
sed -i "s|!APP_URL!|$APP_URL|g" /etc/openoni.ini

# Hack apache to do the RAIS proxying
cp /etc/apache2/sites-available/openoni-orig.conf /etc/apache2/sites-available/openoni.conf
sed -i "s/!RAIS_HOST!/rais/g" /etc/apache2/sites-available/openoni.conf
a2ensite openoni
service apache2 reload

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
