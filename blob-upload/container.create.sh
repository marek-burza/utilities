#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: ./container.create.sh PREFIX"
    echo "Example:"
    echo "./container.create.sh example"
    exit 1
else
    PREFIX=$1
fi


LOCATION=centralus
RESOURCE_GROUP=${PREFIX}resourcegroup
STORAGE_ACCOUNT=${PREFIX}storageaccount
CONTAINER_NAME=${PREFIX}container

az login
az group create --name $RESOURCE_GROUP --location $LOCATION
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_GRS --kind StorageV2 --access-tier Hot
STORAGE_ACCOUNT_KEY=$(az storage account keys list -g $RESOURCE_GROUP -n $STORAGE_ACCOUNT --query [0].value --output tsv)
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --account-key $STORAGE_ACCOUNT_KEY --public-access blob
az storage account show-connection-string --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT
