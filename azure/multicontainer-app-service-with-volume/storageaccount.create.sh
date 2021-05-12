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

# Create storage account
STORAGE_ACCOUNT_EXISTS=$(az storage account check-name --name $STORAGE_ACCOUNT --query nameAvailable)
if [ "$STORAGE_ACCOUNT_EXISTS" = "true" ]; then
  az storage account create --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT --location $LOCATION --sku Standard_LRS --kind StorageV2
fi
