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
export CLUSTER_PRINCIPAL=${PREFIX}principal
export AKS_CLUSTER=${PREFIX}cluster

# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER
# Destroy the files share secret
SECRET_RESULT=$(kubectl get secret -o json | jq -e '.items[].metadata | select(.name == "azure-secret") | .name == "azure-secret"' 2> /dev/null || echo false)
if [ "$SECRET_RESULT" != "true" ]; then
    kubectl delete secret azure-secret
fi
# Destroy the container registry secret
SECRET_RESULT=$(kubectl get secret -o json | jq -e '.items[].metadata | select(.name == "registry-secret") | .name == "registry-secret"' 2> /dev/null || echo false)
if [ "$SECRET_RESULT" != "true" ]; then
    kubectl delete secret registry-secret
fi
# Destroy the cluster
AKS_CLUSTER_RESULT=$(az aks list --resource-group $RESOURCE_GROUP --query "contains([].name, '$AKS_CLUSTER')")
if [ "$AKS_CLUSTER_RESULT" = "true" ]; then
    az aks delete --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER -y
fi
# Destroy the service principal
CLUSTER_PRINCIPAL_RESULT=$(az ad sp list --show-mine --query "contains([].appDisplayName, '$CLUSTER_PRINCIPAL')")
if [ "$CLUSTER_PRINCIPAL_RESULT" = "true" ]; then
    CLUSTER_PRINCIPAL_ID=$(az ad sp list --show-mine --query "[?displayName == '$CLUSTER_PRINCIPAL'].appId" --output tsv)
    az ad sp delete --id $CLUSTER_PRINCIPAL_ID
fi

