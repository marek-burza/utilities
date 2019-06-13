#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: ./container.destroy.sh PREFIX"
    echo "Example:"
    echo "./container.destroy.sh example"
    exit 1
else
    PREFIX=$1
fi


LOCATION=centralus
RESOURCE_GROUP=${PREFIX}resourcegroup
STORAGE_ACCOUNT=${PREFIX}storageaccount
CONTAINER_NAME=${PREFIX}container

az login
STORAGE_ACCOUNT_KEY=$(az storage account keys list -g $RESOURCE_GROUP -n $STORAGE_ACCOUNT --query [0].value --output tsv)
az storage container delete --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --account-key $STORAGE_ACCOUNT_KEY
az storage account delete -y --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP
az group delete -y --name $RESOURCE_GROUP
