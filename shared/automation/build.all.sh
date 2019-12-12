#!/bin/sh

set -e

SELF=$0
BASE=$(dirname "$0")

for ENTRY in $(find . -name "Dockerfile")
do
  /bin/sh $BASE/build.one.sh $ENTRY
done
