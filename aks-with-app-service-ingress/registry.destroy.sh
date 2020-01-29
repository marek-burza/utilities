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

# Destroy the container registry
CONTAINER_REGISTRY_RESULT=$(az acr list --resource-group $RESOURCE_GROUP --query "contains([].name, '$CONTAINER_REGISTRY')")
if [ "$CONTAINER_REGISTRY_RESULT" = "true" ]; then
    az acr delete --resource-group $RESOURCE_GROUP --name $CONTAINER_REGISTRY
fi
