#!/bin/sh

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 PREFIX LOCATION"
    exit 1
else
    PREFIX=$1
    LOCATION=$2
fi


export RESOURCE_GROUP=${PREFIX}rg
export APP=${PREFIX}
export CONTAINER_REGISTRY=${PREFIX}cr
export CONTAINER_IMAGE_TAG=$(git rev-parse --short HEAD)
export STORAGE_VOLUME=${PREFIX}v

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# Do nothing
