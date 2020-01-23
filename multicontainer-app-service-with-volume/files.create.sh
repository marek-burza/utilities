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

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# Obtain storage account connection string
STORAGE_ACCOUNT_CONNECTION_STRING=$(az storage account show-connection-string --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT -o tsv)
# Create files volume
FILES_SHARE_EXISTS=$(az storage share list --account-name $STORAGE_ACCOUNT --query "contains([].name, '$FILES_SHARE')")
if [ "$FILES_SHARE_EXISTS" = "false" ]; then
  az storage share create --name $FILES_SHARE --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
fi
# Transfer files
az storage file upload-batch --source $BASE/web --destination $FILES_SHARE --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
