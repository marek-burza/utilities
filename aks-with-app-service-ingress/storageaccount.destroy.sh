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
export STORAGE_ACCOUNT=${PREFIX}storage

# Destroy the storage account
STORAGE_ACCOUNT_RESULT=$(az storage account check-name --name $STORAGE_ACCOUNT --query nameAvailable)
if [ "$STORAGE_ACCOUNT_RESULT" = "false" ]; then
    az storage account delete --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT -y
fi
