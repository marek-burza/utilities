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

export RESOURCE_GROUP=${PREFIX}group
export CONTAINER_REGISTRY=${PREFIX}registry
export CONTAINER_IMAGE_TAG=$(git rev-parse --short HEAD)
export CONTAINER_IMAGE=${CONTAINER_REGISTRY}.azurecr.io/example:$CONTAINER_IMAGE_TAG

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# Build and upload container image
az acr login --name $CONTAINER_REGISTRY
docker build -t example .
docker tag example $CONTAINER_IMAGE
docker push $CONTAINER_IMAGE
docker rmi example
