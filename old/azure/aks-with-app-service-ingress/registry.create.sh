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

# Create the container registry
CONTAINER_REGISTRY_RESULT=$(az acr list --resource-group $RESOURCE_GROUP --query "contains([].name, '$CONTAINER_REGISTRY')")
if [ "$CONTAINER_REGISTRY_RESULT" = "false" ]; then
    az acr create --resource-group $RESOURCE_GROUP --location $LOCATION --name $CONTAINER_REGISTRY --sku Basic --admin-enabled true
fi
