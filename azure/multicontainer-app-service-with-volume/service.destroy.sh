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

# Destroy container image
az acr repository delete --name $CONTAINER_REGISTRY --image service:$CONTAINER_IMAGE_TAG --yes
