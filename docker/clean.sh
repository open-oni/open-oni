#!/usr/bin/env bash
#
# Stop and remove the docker containers necessary for open ONI
# except for the persistent data containers

for service in openoni-dev openoni-dev-mysql openoni-dev-solr openoni-dev-rais; do
  echo "stopping $service"
  docker stop $service

  echo "removing $service"
  docker rm $service
done

echo "Run ./dev.sh to set your environment back up"
