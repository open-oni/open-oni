#!/usr/bin/env bash
#
# Stop and remove the docker containers necessary for open ONI
# except for the persistent data containers

remove_env() {
  local success1=0
  echo "-- Destroying ENV"
  docker exec -it openoni-dev rm /opt/openoni/ENV -rf && success1=1

  local success2=0
  echo "-- Destroying .python-eggs"
  docker exec -it openoni-dev rm /opt/openoni/.python-eggs -rf && success2=1

  if (( $success1 == 0 || $success2 == 0 )); then
    echo
    echo "Unable to destroy environment!  Aborting!"
    exit
  fi
}

destroy_containers() {
  for service in openoni-dev openoni-dev-mysql openoni-dev-solr openoni-dev-rais; do
    echo "-- Stopping $service"
    docker stop $service >/dev/null

    echo "-- Removing $service"
    docker rm $service >/dev/null
  done
}

remove_data() {
  echo "-- Removing data containers for mysql and solr"
  docker rm openoni-dev-data-mysql openoni-dev-data-solr >/dev/null
  docker volume rm $(docker volume ls -qf dangling=true) >/dev/null
}

clean_pyc() {
  echo "-- Cleaning *.pyc files"
  find . -path "./ENV" -prune -o -name "*.pyc" -print0 | xargs -0 rm -f
}

remove_static() {
  echo "-- Removing .static-media"
  rm -rf .static-media
}

option=${1:-}

if [ "$option" == "--help" ] || [ "$option" == "-h" ]; then
  echo "Usage: ./docker/clean.sh [options]"
  echo "    --apocalypse    destroys data, python packages, and containers"
  echo "    --help          usage output"
  echo "    --nuclear       destroys data and containers"
  echo "Run without options, this script will remove the non-data containers"
  echo "and clear your static-media directory"
  exit
fi

echo "Cleaning in progress..."
echo
echo "Run ./docker/dev.sh to set your environment back up"
echo

# --apocalypse runs all the cleaners and exits
if [ "$option" == "--apocalypse" ]; then
  echo "[1mOMFG[0m IT'S THE APOCALYPSE!"
  echo
  echo "Destroying all data as well as installed Python packages!"
  remove_env
  remove_static
  destroy_containers
  remove_data
  clean_pyc
  exit
fi

# --nuclear removes data and containers, then exits
if [ "$option" == "--nuclear" ]; then
  echo "OMG GOING NUCLEAR!  All your Solr and MySQL data is GONE."
  remove_static
  destroy_containers
  remove_data
  clean_pyc
  exit
fi

# No options means just cleaning non-data containers and *.pyc files; consider
# this similar to a reboot
remove_static
destroy_containers
clean_pyc
