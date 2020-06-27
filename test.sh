#!/usr/bin/env bash

#set -eu

CLEAR=0
PERSIST=0
while getopts "cp" opt; do
  case "${opt}" in
    c) CLEAR=1 ;;
    p) PERSIST=1 ;;
    ?)
      echo "Usage: test.sh [-c|p]"
      echo "  -c Clear - Only clear test containers, images, volumes"
      echo "  -p Persist - Keep containers, images, volumes after tests run"
      exit 1
      ;;
  esac
done
readonly CLEAR
readonly PERSIST

function clear_env {
  docker-compose -f test-compose.yml -p onitest down --rmi=local -v
  rm -rf ENV/
}

echo "Clearing test environment to start from scratch"
clear_env

if [[ ${CLEAR} -eq 1 ]]; then
  exit 0
fi

echo "Building test environment and running tests"
docker-compose -f test-compose.yml -p onitest up test

# Remove test environment unless flag set to persist, presumably to save time
# for repeated test runs
if [[ ${PERSIST} -eq 0 ]]; then
  echo "Removing test environment"
  clear_env
fi

