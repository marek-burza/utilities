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

export RESOURCE_GROUP=${PREFIX}resources
export CLUSTER_PRINCIPAL=${PREFIX}principal
export AKS_CLUSTER=${PREFIX}cluster
export IOT_HUB=${PREFIX}hub
export IOT_EDGE_DEVICE_ID=${PREFIX}prototype

# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER
# Destroy the connection string secret
SECRET_RESULT=$(kubectl get secret -n hub0 -o yaml | yq eval '([.items.[].metadata.name | select(. == "my-secrets")] | length) == 0' -)
if [ "$SECRET_RESULT" = "false" ]; then
    kubectl delete secret my-secrets -n hub0
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

