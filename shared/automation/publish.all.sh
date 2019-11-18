#!/bin/sh

set -e

SELF=$0
BASE=$(dirname "$0")

echo $DOCKERHUB_TOKEN | docker login --username $DOCKERHUB_USER --password-stdin

find $(realpath .) -name "Dockerfile" -exec /bin/sh $BASE/publish.one.sh {} \;
