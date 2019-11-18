#!/bin/sh

set -e

IMAGE=$(basename $(dirname $1))

docker tag $IMAGE $DOCKERHUB_USER/$IMAGE
docker push $DOCKERHUB_USER/$IMAGE
