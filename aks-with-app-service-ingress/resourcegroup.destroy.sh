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

# Destroy the resource group
RESOURCE_GROUP_RESULT=$(az group exists --name $RESOURCE_GROUP)
if [ "$RESOURCE_GROUP_RESULT" != "true" ]; then
    az group delete --name $RESOURCE_GROUP -y
fi
