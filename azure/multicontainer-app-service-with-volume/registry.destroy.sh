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

# Destroy container registry
CONTAINER_REGISTRY_EXISTS=$(az acr list --resource-group $RESOURCE_GROUP --query "contains([].name, '$CONTAINER_REGISTRY')")
if [ "$CONTAINER_REGISTRY_EXISTS" = "true" ]; then
  az acr delete --resource-group $RESOURCE_GROUP --name $CONTAINER_REGISTRY -y
fi
