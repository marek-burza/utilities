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
export CONTAINER_REGISTRY=${PREFIX}cr
export CONTAINER_IMAGE_TAG=$(git rev-parse --short HEAD)
export STORAGE_VOLUME=${PREFIX}v

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if ! command -v jq > /dev/null; then
    echo "Install jq package"
    exit 1
fi
if ! command -v envsubst > /dev/null; then
    echo "Install gettext package"
    exit 1
fi

# Create consumption plan
CONSUMPTION_PLAN_EXISTS=$(az appservice plan list --query "contains([].name, '$CONSUMPTION_PLAN')")
if [ "$CONSUMPTION_PLAN_EXISTS" = "false" ]; then
  az appservice plan create --resource-group $RESOURCE_GROUP --name $CONSUMPTION_PLAN --sku B1 --is-linux
fi
# Create app
envsubst '$CONTAINER_REGISTRY$CONTAINER_IMAGE_TAG$STORAGE_VOLUME' < $BASE/docker-compose.yml.template > $BASE/docker-compose.yml
APP_EXISTS=$(az webapp list --resource-group $RESOURCE_GROUP --query "contains([].name,'$APP')")
if [ "$APP_EXISTS" = "false" ]; then
  PASSWORD=$(az acr credential show --name $CONTAINER_REGISTRY --query "passwords[0].value" --output tsv)
  az webapp create --resource-group $RESOURCE_GROUP --plan $CONSUMPTION_PLAN --name $APP --docker-registry-server-user $CONTAINER_REGISTRY --docker-registry-server-password "$PASSWORD" --multicontainer-config-type compose --multicontainer-config-file $BASE/docker-compose.yml
fi
rm -f $BASE/docker-compose.yml 2> /dev/null || true
# Add CORS
CORS_EXISTS=$(az webapp cors show --resource-group $RESOURCE_GROUP --name $APP --query "allowedOrigins.contains(@, '*')" 2> /dev/null || echo false)
if [ "$CORS_EXISTS" = "false" ]; then
  az webapp cors add --resource-group $RESOURCE_GROUP --name $APP --allowed-origins "*"
fi
# Add Volume
VOLUME_EXISTS=$(az webapp config storage-account list --resource-group $RESOURCE_GROUP --name $APP --query "contains([].name, '$STORAGE_VOLUME')")
if [ "$VOLUME_EXISTS" = "false" ]; then
  STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT --query "[0].value" -o tsv)
  az webapp config storage-account add --resource-group $RESOURCE_GROUP --name $APP --custom-id $STORAGE_VOLUME --storage-type AzureFiles --account-name $STORAGE_ACCOUNT --share-name $FILES_SHARE --access-key "$STORAGE_KEY" --mount-path "/web"
fi
