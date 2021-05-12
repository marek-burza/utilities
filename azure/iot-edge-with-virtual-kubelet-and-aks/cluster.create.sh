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

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# Create the service principal
CLUSTER_PRINCIPAL_RESULT=$(az ad sp list --show-mine --query "contains([].appDisplayName, '$CLUSTER_PRINCIPAL')")
if [ "$CLUSTER_PRINCIPAL_RESULT" = "false" ]; then
    az ad sp create-for-rbac --name http://$CLUSTER_PRINCIPAL --skip-assignment
fi
# Create the cluster
mv $HOME/.azure/aksServicePrincipal.json $HOME/.azure/aksServicePrincipal.json.$(date +"%Y%m%d%H%M%S") || true  # Related to https://docs.microsoft.com/en-us/azure/aks/kubernetes-service-principal#troubleshoot
mv $HOME/.kube $HOME/.kube.$(date +"%Y%m%d%H%M%S") || true
AKS_CLUSTER_RESULT=$(az aks list --resource-group $RESOURCE_GROUP --query "contains([].name, '$AKS_CLUSTER')")
if [ "$AKS_CLUSTER_RESULT" = "false" ]; then
    PASSWORD=$(openssl rand -base64 32)
    CLUSTER_PRINCIPAL_ID=$(az ad app list --query "[?displayName == '$CLUSTER_PRINCIPAL'].appId" --all --output tsv)
    az ad app update --id "$CLUSTER_PRINCIPAL_ID" --password "$PASSWORD" --end-date $(date --date='10 years' +"%Y-%m-%d")
    az aks create --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --node-count 1 --generate-ssh-keys --service-principal "$CLUSTER_PRINCIPAL_ID" --client-secret "$PASSWORD" --node-vm-size Standard_B2s  # Resize node pool to Standard_B1s manually
fi
# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER
# Create the connection string secret
NAMESPACE_RESULT=$(kubectl get namespace -o yaml | yq eval '([.items.[].metadata.name | select(. == "hub0")] | length) == 0' -)
if [ "$NAMESPACE_RESULT" = "true" ]; then
    kubectl create ns hub0
fi
SECRET_RESULT=$(kubectl get secret -n hub0 -o yaml | yq eval '([.items.[].metadata.name | select(. == "my-secrets")] | length) == 0' -)
if [ "$SECRET_RESULT" = "true" ]; then
    CONNECTION_STRING=$(az iot hub device-identity connection-string show --hub-name $IOT_HUB --device-id $IOT_EDGE_DEVICE_ID --output tsv)
    kubectl create secret generic my-secrets -n hub0 "--from-literal=hub0-cs="$CONNECTION_STRING""
fi
