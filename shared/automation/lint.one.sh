#!/bin/sh

set -e

DIRECTORY=$(dirname $1)
export IMAGE=$(basename $DIRECTORY)

cat shared/automation/linting.Dockerfile | envsubst > $DIRECTORY/linting.Dockerfile

docker build -f $DIRECTORY/linting.Dockerfile .

rm $DIRECTORY/linting.Dockerfile
