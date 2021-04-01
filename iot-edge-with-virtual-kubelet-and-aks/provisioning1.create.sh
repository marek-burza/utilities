#!/bin/sh

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 PREFIX LOCATION"
    echo "Example:"
    echo "$0 example centralus"
    exit 1
else
    PREFIX=$1
    LOCATION=$2
fi

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if ! command -v jq > /dev/null; then
    echo "Install jq"
    exit 1
fi
if ! command -v yq > /dev/null; then
    echo "Install yq"
    exit 1
fi
if ! command -v kubectl > /dev/null; then
    echo "Install kubectl"
    exit 1
fi
if ! command -v helm > /dev/null; then
    echo "Install helm"
    exit 1
fi

/bin/sh $BASE/resourcegroup.create.sh $PREFIX $LOCATION

/bin/sh $BASE/iot_edge.create.sh $PREFIX $LOCATION

/bin/sh $BASE/cluster.create.sh $PREFIX $LOCATION
