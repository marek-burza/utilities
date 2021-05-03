#!/bin/sh

if [ ! "$DOCKER_HOST" ]; then
  DOCKER_HOST="host.docker.internal"
fi

/usr/bin/socat "$@"
