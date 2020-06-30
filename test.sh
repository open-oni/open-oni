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
      echo "  -c Clear - Only clear Docker test env; don't run tests"
      echo "  -p Persist - Don't clear Docker test env before or after tests"
      exit 1
      ;;
  esac
done
readonly CLEAR
readonly PERSIST

function clear_env {
  docker-compose -f test-compose.yml -p onitest down --rmi=all -v
  rm -rf ENV/
}

if [[ ${PERSIST} -eq 0 ]]; then
  echo "Clearing test environment to start from scratch"
  clear_env
fi

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

