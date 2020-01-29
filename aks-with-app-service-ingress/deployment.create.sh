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

if [ -z "${EXAMPLE_VARIABLE}" ]; then
    echo "Error: EXAMPLE_VARIABLE must be defined"
    exit 1
fi

export RESOURCE_GROUP=${PREFIX}group
export CONTAINER_REGISTRY=${PREFIX}registry
export AKS_CLUSTER=${PREFIX}cluster
export CONTAINER_IMAGE_TAG=$(git rev-parse --short HEAD)
export FILES_SHARE_NAME=${PREFIX}share

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if ! command -v jq > /dev/null; then
    echo "Install gettext package"
    exit 1
fi
if ! command -v nmap > /dev/null; then
    echo "Install nmap package"
    exit 1
fi
if ! command -v envsubst > /dev/null; then
    echo "Install gettext package"
    exit 1
fi
if ! command -v kubectl > /dev/null; then
    echo "Install kubectl"
    exit 1
fi

# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER
# Create the services
PRESENCE_RESULT=$(kubectl get service -o json | jq -e '.items[].metadata | select(.name == "example") | .name == "example"' 2> /dev/null || echo false)
if [ "$PRESENCE_RESULT" = "true" ]; then
    CANDIDATE=$(kubectl get service example -o json | jq -r '.status.loadBalancer.ingress[0].ip')
    while [ "$CANDIDATE" = "<pending>" ]; do
        sleep 1
        CANDIDATE=$(kubectl get service example -o json | jq -r '.status.loadBalancer.ingress[0].ip')
    done
    export LB_IP=$CANDIDATE
else
    AKS_CLUSTER_RESOURCE_GROUP=$(az aks show --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --query "nodeResourceGroup" --output tsv)
    AKS_CLUSTER_VNET=$(az network vnet list --resource-group $AKS_CLUSTER_RESOURCE_GROUP --query "[0].name" --output tsv)
    AKS_CLUSTER_LB_CIDR=$(az network vnet subnet list --resource-group $AKS_CLUSTER_RESOURCE_GROUP --vnet-name $AKS_CLUSTER_VNET --query "[?name == 'aks-subnet'].addressPrefix" --output tsv)
    for CANDIDATE in $(nmap -sL -n "$AKS_CLUSTER_LB_CIDR" | grep 'for' | sed 's/Nmap.*for\ //g'); do
        AVAILABLE_RESULT=$(az network vnet check-ip-address --resource-group $AKS_CLUSTER_RESOURCE_GROUP --name $AKS_CLUSTER_VNET --ip-address $CANDIDATE --query "available")
        if [ "$AVAILABLE_RESULT" = "true" ]; then
            export LB_IP=$CANDIDATE
            break
        fi
    done
fi
envsubst '$CONTAINER_REGISTRY$CONTAINER_IMAGE_TAG$FILES_SHARE_NAME$LB_IP$EXAMPLE_VARIABLE' < $BASE/aks.kubernetes.config.yml.template > $BASE/aks.kubernetes.config.yml
kubectl apply -f $BASE/aks.kubernetes.config.yml
