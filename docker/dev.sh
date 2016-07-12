#!/bin/bash
#
# This should be run from the app root directory, not docker/.  It's just in
# here to keep all the docker stuff centralized.
#
# Example usage:
#
#     cd /path/to/open-oni
#     export APP_URL="http://192.168.56.99"
#     ./docker/dev.sh

set -u

DB_READY=0
MAX_TRIES=50
MYSQL_ROOT_PASSWORD=123456

PORT=${DOCKERPORT:-80}

APP_URL=${APP_URL:-}
if [ -z "$APP_URL" ]; then
  echo "Please set the APP_URL environment variable"
  echo "e.g., 'export APP_URL=\"http://192.168.56.99\"'"
  exit -1

  if [ $PORT != 80 ]; then
    APP_URL=$APP_URL:$PORT
  fi
fi

SOLR=4.10.4
SOLRDELAY=${SOLRDELAY:-10} # interval to wait for dependent docker services to initialize
TRIES=0

docker stop openoni-dev || true
docker rm openoni-dev || true

# $1 = name of container, $2 = container running status
container_start () {
  echo "Existing $1 container found"
  if [ "$2" == "false" ]; then
    docker start $1
  fi
}

# Make sure settings_local.py exists so the app doesn't crash
if [ ! -f settings_local.py ]; then
  touch settings_local.py
fi

# Make persistent data containers
# If these containers are removed, you will lose all mysql and solr data
MYSQL_DATA_STATUS=$(docker inspect --type=container --format="{{ .State.Running }}" openoni-dev-data-mysql 2> /dev/null)
if [ -z "$MYSQL_DATA_STATUS" ]; then
  echo "Creating a data container for mysql ..."
  docker create -v /var/lib/mysql --name openoni-dev-data-mysql mysql
fi
SOLR_DATA_STATUS=$(docker inspect --type=container --format="{{ .State.Running }}" openoni-dev-data-solr 2> /dev/null)
if [ -z "$SOLR_DATA_STATUS" ]; then
  echo "Creating a data container for solr ..."
  docker create -v /opt/solr --name openoni-dev-data-solr makuk66/docker-solr:$SOLR
fi

# Make containers for mysql and solr
echo "Building openoni for development"
docker build -t open-oni:dev -f docker/Dockerfile-dev docker/

# Copy latest openoni MySQL config into directory with dev overrides
cp $(pwd)/conf/mysql/openoni.cnf $(pwd)/docker/mysql/

MYSQL_STATUS=$(docker inspect --type=container --format="{{ .State.Running }}" openoni-dev-mysql 2> /dev/null)
if [ -z "$MYSQL_STATUS" ]; then
  echo "Starting mysql ..."
  docker run -d \
    --name openoni-dev-mysql \
    -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
    -e MYSQL_DATABASE=openoni \
    -e MYSQL_USER=openoni \
    -e MYSQL_PASSWORD=openoni \
    --volumes-from openoni-dev-data-mysql \
    -v /$(pwd)/docker/mysql:/etc/mysql/conf.d:Z \
    mysql

  while [ $DB_READY == 0 ]
  do
   if
     ! docker exec openoni-dev-mysql mysql -uroot -p$MYSQL_ROOT_PASSWORD \
       -e 'ALTER DATABASE openoni charset=utf8' > /dev/null 2>/dev/null
   then
     sleep 5
     let TRIES++
     echo "Looks like we're still waiting for MySQL ... 5 more seconds ... retry $TRIES of $MAX_TRIES"
     if [ "$TRIES" = "$MAX_TRIES" ]
     then
      echo "Looks like we couldn't get MySQL running. Could you check settings and try again?"
      exit 2
     fi
   else
     DB_READY=1
   fi
  done

  # set up access to a test database, for masochists
  echo "setting up a test database ..."
  docker exec openoni-dev-mysql mysql -u root --password=$MYSQL_ROOT_PASSWORD -e 'USE mysql;
  GRANT ALL on test_openoni.* TO "openoni"@"%" IDENTIFIED BY "openoni";';
else
  container_start "openoni-dev-mysql" $MYSQL_STATUS
fi

SOLR_STATUS=$(docker inspect --type=container --format="{{ .State.Running }}" openoni-dev-solr 2> /dev/null)
if [ -z "$SOLR_STATUS" ]; then
  echo "Starting solr ..."
  docker run -d \
    --name openoni-dev-solr \
    -v $(pwd)/docker/solr/schema.xml:/opt/solr/example/solr/collection1/conf/schema.xml:Z \
    -v $(pwd)/docker/solr/solrconfig.xml:/opt/solr/example/solr/collection1/conf/solrconfig.xml:Z \
    --volumes-from openoni-dev-data-solr \
    makuk66/docker-solr:$SOLR && sleep $SOLRDELAY
else
  container_start "openoni-dev-solr" $SOLR_STATUS
fi

RAIS_STATUS=$(docker inspect --type=container --format="{{ .State.Running }}" openoni-dev-rais 2> /dev/null)
if [ -z "$RAIS_STATUS" ]; then
  echo "Starting RAIS ..."
  docker run -d \
    --name openoni-dev-rais \
    -e RAIS_IIIFURL="$APP_URL/images/iiif" \
    -e IIIFURL="$APP_URL/images/iiif" \
    -v $(pwd)/docker/data/batches:/var/local/images:z \
    uolibraries/rais:2.6

else
  container_start "openoni-dev-rais" $RAIS_STATUS
fi

echo "Starting openoni for development ..."
# Make sure subdirs are built
mkdir -p data/batches data/cache data/bib
docker run -itd \
  -p $PORT:80 \
  -e APP_URL=$APP_URL \
  --name openoni-dev \
  --link openoni-dev-mysql:db \
  --link openoni-dev-solr:solr \
  --link openoni-dev-rais:rais \
  -v $(pwd):/opt/openoni:Z \
  -v $(pwd)/docker/data:/opt/openoni/data:z \
  open-oni:dev
