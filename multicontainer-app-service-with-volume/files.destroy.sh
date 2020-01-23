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
export STORAGE_ACCOUNT=${PREFIX}sa
export FILES_SHARE=${PREFIX}share

# Obtain storage account connection string
STORAGE_ACCOUNT_CONNECTION_STRING=$(az storage account show-connection-string --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT -o tsv)
# Destroy files volume
FILES_SHARE_EXISTS=$(az storage share list --account-name $STORAGE_ACCOUNT --query "contains([].name, '$FILES_SHARE')")
if [ "$FILES_SHARE_EXISTS" = "true" ]; then
  az storage share delete --name $FILES_SHARE --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
fi
