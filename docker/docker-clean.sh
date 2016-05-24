#!/usr/bin/env bash
#
# Stop and remove the docker containers necessary for open ONI
# except for the persistent data containers

echo "stopping ..."
docker stop openoni-dev
docker stop openoni-dev-mysql
docker stop openoni-dev-solr

echo "removing ..."
docker rm openoni-dev
docker rm openoni-dev-mysql
docker rm openoni-dev-solr

echo "Run ./dev.sh to set your environment back up"
