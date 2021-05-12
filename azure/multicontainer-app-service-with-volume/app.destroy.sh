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
export CONSUMPTION_PLAN=${PREFIX}cp
export APP=${PREFIX}

# Destroy the app
APP_EXISTS=$(az webapp list --resource-group $RESOURCE_GROUP --query "contains([].name,'$APP')")
if [ "$APP_EXISTS" = "true" ]; then
  az webapp delete --resource-group $RESOURCE_GROUP --name $APP
fi
# Destroy the consumption plan
CONSUMPTION_PLAN_EXISTS=$(az appservice plan list --resource-group $RESOURCE_GROUP --query "contains([].name, '$CONSUMPTION_PLAN')")
if [ "$CONSUMPTION_PLAN_EXISTS" = "true" ]; then
  az appservice plan delete --resource-group $RESOURCE_GROUP --name $CONSUMPTION_PLAN -y
fi

