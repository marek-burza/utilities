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
export FILES_SHARE_NAME=${PREFIX}share
export CONTAINER_REGISTRY=${PREFIX}registry
export CONSUMPTION_PLAN=${PREFIX}consumptionplan
export APP=${PREFIX}app
export AD_NAME=${PREFIX}ad

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# az login
# Destroy the function app
APP_RESULT=$(az webapp list --resource-group $RESOURCE_GROUP --query "contains([].name,'$APP')")
if [ "$APP_RESULT" = "true" ]; then
    az webapp delete --name $APP --resource-group $RESOURCE_GROUP
fi
# Destroy the consumption plan
CONSUMPTION_PLAN_RESULT=$(az functionapp plan list --query "contains([].name, '$CONSUMPTION_PLAN')")
if [ "$CONSUMPTION_PLAN_RESULT" = "true" ]; then
    az functionapp plan delete --resource-group $RESOURCE_GROUP --name $CONSUMPTION_PLAN -y
fi
# Destroy Authentication / Authorization of the function app
AAD_ID=$(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
if [ "$AAD_ID" != "" ]; then
    az ad app delete --id $(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
fi
# Destroy the container registry
CONTAINER_REGISTRY_RESULT=$(az acr list --resource-group $RESOURCE_GROUP --query "contains([].name, '$CONTAINER_REGISTRY')")
if [ "$CONTAINER_REGISTRY_RESULT" = "true" ]; then
    az acr delete --resource-group $RESOURCE_GROUP --name $CONTAINER_REGISTRY -y
fi
# Destroy the files volume
STORAGE_ACCOUNT_CONNECTION_STRING=$(az storage account show-connection-string --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT -o tsv)
FILES_SHARE_RESULT=$(az storage share list --account-name $STORAGE_ACCOUNT --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING --query "contains([].name, '$FILES_SHARE_NAME')")
if [ "$FILES_SHARE_RESULT" = "true" ]; then
    az storage share delete --name $FILES_SHARE_NAME --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
fi
# Destroy the storage account
STORAGE_ACCOUNT_RESULT=$(az storage account check-name --name $STORAGE_ACCOUNT --query nameAvailable)
if [ "$STORAGE_ACCOUNT_RESULT" = "false" ]; then
    az storage account delete --name $STORAGE_ACCOUNT --resource-group $RESOURCE_GROUP -y
fi
# Destroy the resource group
RESOURCE_GROUP_RESULT=$(az group exists --name $RESOURCE_GROUP)
if [ "$RESOURCE_GROUP_RESULT" = "true" ]; then
    az group delete --name $RESOURCE_GROUP -y
fi
# Clean-up
rm $BASE/date.txt 2> /dev/null || true
