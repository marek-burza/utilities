#!/bin/sh

set -e

SELF=$0
BASE=$(dirname "$0")

find $(realpath .) -name "Dockerfile" -exec /bin/sh $BASE/build.one.sh {} \;
