#!/bin/bash

export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
mkdir -p /var/tmp/django_cache && chown -R www-data:www-data /var/tmp/django_cache

if [ ! -d /opt/openoni/ENV ]; then
  /pip-install.sh
fi

# Generate a random secret key if that hasn't already happened.  This stays the
# same after it's first set.
sed -i "s/!SECRET_KEY!/$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 80)/g" /etc/openoni.ini.orig

# Refresh the environmental config for DB and Solr hosts in case of IP changes
cp /etc/openoni.ini.orig /etc/openoni.ini
sed -i "s/!DB_HOST!/$DB_PORT_3306_TCP_ADDR/g" /etc/openoni.ini
sed -i "s/!SOLR_HOST!/$SOLR_PORT_8983_TCP_ADDR/g" /etc/openoni.ini
sed -i "s|!APP_URL!|$APP_URL|g" /etc/openoni.ini

# Hack apache to do the RAIS proxying
cp /etc/apache2/sites-available/openoni-orig.conf /etc/apache2/sites-available/openoni.conf
sed -i "s/!RAIS_HOST!/$RAIS_PORT_12415_TCP_ADDR/g" /etc/apache2/sites-available/openoni.conf
a2ensite openoni
service apache2 reload

cd /opt/openoni
source ENV/bin/activate
django-admin.py syncdb --noinput
django-admin.py openoni_sync
django-admin.py collectstatic --noinput

# Remove any pre-existing PID file which prevents Apache from starting
#   thus causing the container to close immediately after
#   See: https://github.com/docker-library/php/pull/59
rm -f /var/run/apache2/apache2.pid

source /etc/apache2/envvars
exec apache2 -D FOREGROUND

