#!/bin/bash

set -u

DB_READY=0
MAX_TRIES=50
MYSQL_ROOT_PASSWORD=123456

PORT=${DOCKERPORT:-80}

APP_URL=${APP_URL:-}
if [ -z "$APP_URL" ]; then
  if [ $(command -v docker-machine) ]; then
    ip=$(docker-machine ip default)
    APP_URL="http://$ip"
  else
    echo "Please set the APP_URL environment variable"
    exit -1
  fi

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
if [ ! -f open-oni/settings_local.py ]; then
  touch open-oni/settings_local.py
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
docker build -t open-oni:dev -f Dockerfile-dev .

# Copy latest openoni MySQL config into directory with dev overrides
cp $(pwd)/open-oni/conf/mysql/openoni.cnf $(pwd)/mysql/

MYSQL_STATUS=$(docker inspect --type=container --format="{{ .State.Running }}" openoni-dev-mysql 2> /dev/null)
if [ -z "$MYSQL_STATUS" ]; then
  echo "Starting mysql ..."
  docker run -d \
    -p 3306:3306 \
    --name openoni-dev-mysql \
    -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
    -e MYSQL_DATABASE=openoni \
    -e MYSQL_USER=openoni \
    -e MYSQL_PASSWORD=openoni \
    --volumes-from openoni-dev-data-mysql \
    -v /$(pwd)/mysql:/etc/mysql/conf.d:Z \
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
    -p 8983:8983 \
    --name openoni-dev-solr \
    -v /$(pwd)/solr/schema.xml:/opt/solr/example/solr/collection1/conf/schema.xml:Z \
    -v /$(pwd)/solr/solrconfig.xml:/opt/solr/example/solr/collection1/conf/solrconfig.xml:Z \
    --volumes-from openoni-dev-data-solr \
    makuk66/docker-solr:$SOLR && sleep $SOLRDELAY
else
  container_start "openoni-dev-solr" $SOLR_STATUS
fi

RAIS_STATUS=$(docker inspect --type=container --format="{{ .State.Running }}" openoni-dev-rais 2> /dev/null)
if [ -z "$RAIS_STATUS" ]; then
  echo "Starting RAIS ..."
  docker run -d \
    -p 12415:12415 \
    --name openoni-dev-rais \
    -e TILESIZES=512,1024 \
    -e IIIFURL="$APP_URL/images/iiif" \
    -e PORT=12415 \
    -v $(pwd)/data/batches:/var/local/images:z \
    uolibraries/rais

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
  -v $(pwd)/open-oni:/opt/openoni:Z \
  -v $(pwd)/data:/opt/openoni/data:z \
  open-oni:dev

docker logs -f openoni-dev

