#!/usr/bin/env bash

#pause django until mysql start
HOST="$1"
shift
CMD="$@"

until nc -z ${HOST%:*} ${HOST#*:}; do
  echo "Waiting for $HOST..."
  sleep 2
done

exec $CMD