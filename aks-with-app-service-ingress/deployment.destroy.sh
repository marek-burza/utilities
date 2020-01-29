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
export CONTAINER_REGISTRY=${PREFIX}registry
export AKS_CLUSTER=${PREFIX}cluster
export CONTAINER_IMAGE_TAG=$(git rev-parse --short HEAD)
export FILES_SHARE_NAME=${PREFIX}share

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if ! command -v kubectl > /dev/null; then
    echo "Install kubectl"
    exit 1
fi

# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER
# Destroy the services
kubectl delete services example
