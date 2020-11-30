#!/bin/sh

set -e

SELF=$0
BASE=$(dirname "$0")

for ENTRY in $(find . -name "Dockerfile")
do
  DIRECTORY=$(dirname $ENTRY)
  NAME=$(basename $DIRECTORY)
  IMAGE=$GITHUB_ACTOR/$NAME:latest
  echo "Building & Publishing: $IMAGE"
  cd $DIRECTORY
  docker build -t $NAME .
  docker tag $NAME $IMAGE
  docker push $IMAGE
  cd $BASE
done