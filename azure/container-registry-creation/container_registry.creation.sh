#!/bin/sh

# Check input arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: ./container_registry.creation.sh RESOURCE_GROUP LOCATION CONTAINER_REGISTRY CONTAINER_REGISTRY_SKU"
    echo "Arguments:"
    echo "    RESOURCE_GROUP           - Name of the resource group"
    echo "    LOCATION                 - Location for the resources"
    echo "    CONTAINER_REGISTRY       - Name of the container registry"
    echo "    CONTAINER_REGISTRY_SKU   - SKU of the container registry"
    echo "Example:"
    echo "./container_registry.creation.sh someresourcegroup westus somecontainerregistry Basic"
    exit 1
else
    RESOURCE_GROUP=$1
    LOCATION=$2
    CONTAINER_REGISTRY=$3
    CONTAINER_REGISTRY_SKU=$4
fi

# Log in
az login --service-principal -u $AZURE_USER -p $AZURE_PASSWORD --tenant $AZURE_TENANT || exit

# Create resource group if necessary
RESOURCE_GROUP_RESULT=$(az group exists --name $RESOURCE_GROUP)
if [ "$RESOURCE_GROUP_RESULT" != "true" ]; then
  az group create --location $LOCATION --name $RESOURCE_GROUP
fi

# Create container registry if necessary
az acr show --name $CONTAINER_REGISTRY
CONTAINER_REGISTRY_RESULT=$?
if [ "$CONTAINER_REGISTRY_RESULT" != "0" ]; then
  az acr create --name $CONTAINER_REGISTRY --resource-group $RESOURCE_GROUP --location $LOCATION --sku $CONTAINER_REGISTRY_SKU
fi
