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
export FILES_SHARE_NAME=${PREFIX}share

# Obtain storage account connection string
STORAGE_ACCOUNT_CONNECTION_STRING=$(az storage account show-connection-string --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT -o tsv)
# Destroy the files share
FILES_SHARE_RESULT=$(az storage share list --account-name $STORAGE_ACCOUNT --query "contains([].name, '$FILES_SHARE_NAME')" --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING)
if [ "$FILES_SHARE_RESULT" = "true" ]; then
    az storage share delete --name $FILES_SHARE_NAME --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
fi
