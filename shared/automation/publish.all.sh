#!/bin/sh

set -e

SELF=$0
BASE=$(dirname "$0")

echo $DOCKERHUB_TOKEN | docker login --username $DOCKERHUB_USER --password-stdin

for ENTRY in $(find . -name "Dockerfile")
do
  /bin/sh $BASE/publish.one.sh $ENTRY
done

docker logout
