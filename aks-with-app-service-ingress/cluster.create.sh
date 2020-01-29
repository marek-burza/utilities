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
export CONTAINER_REGISTRY=${PREFIX}registry
export CLUSTER_PRINCIPAL=${PREFIX}principal
export AKS_CLUSTER=${PREFIX}cluster

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

# Create the service principal
CLUSTER_PRINCIPAL_RESULT=$(az ad sp list --show-mine --query "contains([].appDisplayName, '$CLUSTER_PRINCIPAL')")
if [ "$CLUSTER_PRINCIPAL_RESULT" = "false" ]; then
    az ad sp create-for-rbac --name http://$CLUSTER_PRINCIPAL --skip-assignment
fi
# Create the cluster
AKS_CLUSTER_RESULT=$(az aks list --resource-group $RESOURCE_GROUP --query "contains([].name, '$AKS_CLUSTER')")
if [ "$AKS_CLUSTER_RESULT" = "false" ]; then
    PASSWORD=$(openssl rand -base64 32)
    CLUSTER_PRINCIPAL_ID=$(az ad app list --query "[?displayName == '$CLUSTER_PRINCIPAL'].appId" --all --output tsv)
    az ad app update --id "$CLUSTER_PRINCIPAL_ID" --password "$PASSWORD" --end-date $(date --date='10 years' +"%Y-%m-%d")
    az aks create --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --node-count 1 --generate-ssh-keys --service-principal "$CLUSTER_PRINCIPAL_ID" --client-secret "$PASSWORD" --node-vm-size Standard_B2s  # Resize node pool to Standard_B1s manually
fi
# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER
# Create the container registry secret
SECRET_RESULT=$(kubectl get secret -o json | jq -e '.items[].metadata | select(.name == "registry-secret") | .name == "registry-secret"' 2> /dev/null || echo false)
if [ "$SECRET_RESULT" != "true" ]; then
    PASSWORD=$(az acr credential show --name $CONTAINER_REGISTRY --query "passwords[0].value" --output tsv)
    kubectl create secret docker-registry registry-secret --docker-server=$CONTAINER_REGISTRY.azurecr.io --docker-username=$CONTAINER_REGISTRY --docker-password=$PASSWORD --docker-email="noreply@microsoft.com"
fi
# Create the files share secret
SECRET_RESULT=$(kubectl get secret -o json | jq -e '.items[].metadata | select(.name == "azure-secret") | .name == "azure-secret"' 2> /dev/null || echo false)
if [ "$SECRET_RESULT" != "true" ]; then
    STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT --query "[0].value" -o tsv)
    kubectl create secret generic azure-secret --from-literal=azurestorageaccountname=$STORAGE_ACCOUNT --from-literal=azurestorageaccountkey=$STORAGE_KEY
fi
