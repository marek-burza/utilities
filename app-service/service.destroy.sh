#!/bin/sh

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: ./service.destroy.sh PREFIX LOCATION"
    echo "Example:"
    echo "./service.destroy.sh example centralus"
    exit 1
else
    PREFIX=$1
    LOCATION=$2
fi


export RESOURCE_GROUP=${PREFIX}resourcegroup
export STORAGE_ACCOUNT=${PREFIX}storageaccount
export CONTAINER_NAME=${PREFIX}container
export APP=${PREFIX}app
export AD_NAME=${PREFIX}ad

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# az login
# Destroy Authentication / Authorization of the function app
az ad app delete --id $(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
# Destroy the function app
az functionapp delete --name $APP --resource-group $RESOURCE_GROUP
# Destroy the static content container
az storage container delete --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT
# Destroy the storage account
az storage account delete --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP -y
# Destroy the resource group
az group delete --name $RESOURCE_GROUP -y
# Clean-up
rm -rf $BASE/.azurefunctions || true
rm $BASE/proxies.json $BASE/function.zip $BASE/swagger-client.js || true
