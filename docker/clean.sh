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

nuclear=${1:-}
if [ "$nuclear" == "--nuclear" ]; then
  echo "OMG GOING NUCLEAR!  All your Solr and MySQL data is GONE."
  docker rm openoni-dev-data-mysql openoni-dev-data-solr
  docker volume rm $(docker volume ls -qf dangling=true)
fi

echo "Run ./docker/dev.sh to set your environment back up"
