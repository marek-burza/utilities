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
export APP=${PREFIX}
export CONTAINER_REGISTRY=${PREFIX}cr
export CONTAINER_IMAGE_TAG=$(git rev-parse --short HEAD)
export STORAGE_VOLUME=${PREFIX}v

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if ! command -v envsubst > /dev/null; then
    echo "Install gettext package"
    exit 1
fi

# Deploy
envsubst '$CONTAINER_REGISTRY$CONTAINER_IMAGE_TAG$STORAGE_VOLUME' < $BASE/docker-compose.yml.template > $BASE/docker-compose.yml
PASSWORD=$(az acr credential show --name $CONTAINER_REGISTRY --query "passwords[0].value" --output tsv)
az webapp config container set --resource-group $RESOURCE_GROUP --name $APP --docker-registry-server-url https://$CONTAINER_REGISTRY.azurecr.io --docker-registry-server-user $CONTAINER_REGISTRY --docker-registry-server-password "$PASSWORD" --multicontainer-config-type compose --multicontainer-config-file $BASE/docker-compose.yml
