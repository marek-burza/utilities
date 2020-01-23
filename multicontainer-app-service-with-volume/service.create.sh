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
export CONTAINER_REGISTRY=${PREFIX}cr
export CONTAINER_IMAGE_TAG=$(git rev-parse --short HEAD)
export CONTAINER_IMAGE=${CONTAINER_REGISTRY}.azurecr.io/service:$CONTAINER_IMAGE_TAG

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# Build and push container image
az acr login --name $CONTAINER_REGISTRY
docker build -t service .
docker tag service $CONTAINER_IMAGE
docker push $CONTAINER_IMAGE
docker rmi service
