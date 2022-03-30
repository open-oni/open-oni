#!/bin/bash

verify_config() {
  # Make sure settings_local.py exists so the app doesn't crash
  if [ ! -f onisite/settings_local.py ]; then
    cp onisite/settings_local_example.py onisite/settings_local.py
  fi
  # Make sure we have a default urls.py
  if [ ! -f onisite/urls.py ]; then
    cp onisite/urls_example.py onisite/urls.py
  fi

  # Install Python dependencies
  /pip-install.sh
}

setup_database() {
  DB_READY=0
  MAX_TRIES=30
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
  source ENV/bin/activate
  /opt/openoni/manage.py migrate
}

setup_index() {
  echo "Installing Solr configs" >&2
  source ENV/bin/activate
  /opt/openoni/manage.py setup_index
}

prep_webserver() {
  mkdir -p /var/tmp/django_cache && chown -R www-data:www-data /var/tmp/django_cache
  mkdir -p /opt/openoni/log

  # Update Apache config
  cp /opt/openoni/docker/apache/openoni.conf /etc/apache2/sites-available/openoni.conf

  # Set Apache log level from APACHE_LOG_LEVEL in .env file
  sed -i "s/!LOGLEVEL!/$APACHE_LOG_LEVEL/g" /etc/apache2/sites-available/openoni.conf

  # Enable updated Apache config
  a2ensite openoni

  # Get static files ready for Apache to serve
  cd /opt/openoni
  source ENV/bin/activate

  echo "-------" >&2
  echo "Running collectstatic" >&2
  # Django needs write access to STATIC_ROOT and the log directory
  chown -R www-data:www-data /opt/openoni/static/compiled
  chown -R www-data:www-data /opt/openoni/log
  /opt/openoni/manage.py collectstatic --noinput

  # Remove any pre-existing PID file which prevents Apache from starting thus
  # causing the container to close immediately after.
  #
  # See: https://github.com/docker-library/php/pull/59
  rm -f /var/run/apache2/apache2.pid
}

run_apache() {
  echo "ONI setup successful; starting Apache"
  source /etc/apache2/envvars
  exec apache2 -D FOREGROUND
}
