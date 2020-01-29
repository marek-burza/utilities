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
export STORAGE_CONTAINER_NAME=${PREFIX}container
export CONSUMPTION_PLAN=${PREFIX}plan
export APP=${PREFIX}app
export AD_NAME=${PREFIX}ad

# Destroy the app
APP_RESULT=$(az functionapp list --resource-group $RESOURCE_GROUP --query "contains([].name,'$APP')")
if [ "$APP_RESULT" = "true" ]; then
    az functionapp delete --resource-group $RESOURCE_GROUP --name $APP
fi
# Destroy the consumption plan
CONSUMPTION_PLAN_RESULT=$(az appservice plan list --resource-group $RESOURCE_GROUP --query "contains([].name, '$CONSUMPTION_PLAN')")
if [ "$CONSUMPTION_PLAN_RESULT" = "true" ]; then
    az appservice plan delete --resource-group $RESOURCE_GROUP --name $CONSUMPTION_PLAN -y
fi
# Destroy the authentication / authorization client of the function app
AAD_ID=$(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
if [ "$AAD_ID" != "" ]; then
    az ad app delete --id $(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
fi
