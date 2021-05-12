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

# Destroy the container image
az acr repository delete --name $CONTAINER_REGISTRY --image example:$CONTAINER_IMAGE_TAG --yes
