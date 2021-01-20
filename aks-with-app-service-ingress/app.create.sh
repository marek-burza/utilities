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
export AKS_CLUSTER=${PREFIX}cluster
export DELEGATED_SUBNET=${PREFIX}delegated
export STORAGE_ACCOUNT=${PREFIX}storage
export CONSUMPTION_PLAN=${PREFIX}plan
export APP=${PREFIX}app
export AD_NAME=${PREFIX}ad
export VNET_INTEGRATION=${PREFIX}integration

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if ! command -v nmap > /dev/null; then
    echo "Install nmap package"
    exit 1
fi
if ! command -v jq > /dev/null; then
    echo "Install jq package"
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
sudo /usr/bin/pip3 install --system decorator

# Create the consumption plan
CONSUMPTION_PLAN_RESULT=$(az functionapp plan list --query "contains([].name, '$CONSUMPTION_PLAN')")
if [ "$CONSUMPTION_PLAN_RESULT" = "false" ]; then
    az functionapp plan create --resource-group $RESOURCE_GROUP --name $CONSUMPTION_PLAN --sku S1
fi
# Create the app
APP_RESULT=$(az functionapp list --resource-group $RESOURCE_GROUP --query "contains([].name,'$APP')")
if [ "$APP_RESULT" = "false" ]; then
    az functionapp create --resource-group $RESOURCE_GROUP --storage-account $STORAGE_ACCOUNT --plan $CONSUMPTION_PLAN --name $APP
fi
# Create the authentication / authorization client of the function app
AAD_ID=$(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
if [ "$AAD_ID" = "" ]; then
    PASSWORD=$(openssl rand -base64 32)
    az ad app create --display-name $AD_NAME --password $PASSWORD --end-date $(date --date='10 years' +"%Y-%m-%d") --native-app false --homepage https://$APP.azurewebsites.net --identifier-uris https://$APP.azurewebsites.net --reply-urls https://$APP.azurewebsites.net/.auth/login/aad/callback --required-resource-accesses @manifest.sign_in_and_read_user_profile.json
fi
# Proxy slash decoding
az functionapp config appsettings set --resource-group $RESOURCE_GROUP --name $APP --settings AZURE_FUNCTION_PROXY_BACKEND_URL_DECODE_SLASHES=true
# Add auth to the function app
PASSWORD=$(openssl rand -base64 32)
AAD_ID=$(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
AAD_URL=$(az cloud show --query ["endpoints.activeDirectory"][0] --output tsv)
TENNANT_ID=$(az account show --query ["tenantId"][0] --output tsv)
TOKEN_ISSUER=$(curl -s $AAD_URL/$TENNANT_ID/.well-known/openid-configuration | jq -r '.issuer')
az ad app update --id "$AAD_ID" --password "$PASSWORD" --end-date $(date --date='10 years' +"%Y-%m-%d")
az webapp auth update \
    --resource-group $RESOURCE_GROUP \
    --name $APP \
    --enabled true \
    --action LoginWithAzureActiveDirectory \
    --aad-allowed-token-audiences https://$APP.azurewebsites.net/.auth/login/aad/callback \
    --aad-client-id $AAD_ID \
    --aad-client-secret "$PASSWORD" \
    --aad-token-issuer-url $TOKEN_ISSUER
# CORS
CORS_RESULT=$(az functionapp cors show --resource-group $RESOURCE_GROUP --name $APP --query "allowedOrigins.contains(@, '*')")
if [ "$CORS_RESULT" = "false" ]; then
    az functionapp cors add --resource-group $RESOURCE_GROUP --name $APP --allowed-origins "*"
fi
# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER
# Look-up load balancer IP
CANDIDATE=$(kubectl get service example -o json | jq -r '.status.loadBalancer.ingress[0].ip')
while [ "$CANDIDATE" = "<pending>" ]; do
    sleep 1
    CANDIDATE=$(kubectl get service example -o json | jq -r '.status.loadBalancer.ingress[0].ip')
done
# Deploy the app
cd $BASE
LB_IP=$CANDIDATE envsubst '$LB_IP' < $BASE/proxies.json.template > $BASE/proxies.json
zip -r function.zip host.json proxies.json
az functionapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $APP --src function.zip
rm function.zip proxies.json
# Create the subnet for delegation
AKS_CLUSTER_RESOURCE_GROUP=$(az aks show --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --query "nodeResourceGroup" --output tsv)
AKS_CLUSTER_VNET=$(az network vnet list --resource-group $AKS_CLUSTER_RESOURCE_GROUP --query "[0].name" --output tsv)
AKS_CLUSTER_CIDR=$(az network vnet show --name $AKS_CLUSTER_VNET --resource-group $AKS_CLUSTER_RESOURCE_GROUP --query "addressSpace.addressPrefixes[0]" --output tsv)
DELEGATED_SUBNET_RESULT=$(az network vnet subnet list --resource-group $AKS_CLUSTER_RESOURCE_GROUP --vnet-name $AKS_CLUSTER_VNET --query "contains([].name, '$DELEGATED_SUBNET')")
if [ "$DELEGATED_SUBNET_RESULT" = "false" ]; then
    for CANDIDATE in $(nmap -sL -n "$AKS_CLUSTER_CIDR" | grep 'for.*\.0$' | grep -v '\.0\.' | sed 's/Nmap.*for\ //g'); do
        az network vnet subnet create --resource-group $AKS_CLUSTER_RESOURCE_GROUP --vnet-name $AKS_CLUSTER_VNET --name $DELEGATED_SUBNET --address-prefixes "$CANDIDATE/24" --delegations 'Microsoft.Web/serverFarms' || continue
        break
    done
fi
# Configure the virtual net integration
VNET_INTEGRATION_RESULT=$(az functionapp vnet-integration list --resource-group $RESOURCE_GROUP --name $APP --query "contains([].name,'$VNET_INTEGRATION')" 2> /dev/null)
if [ "$VNET_INTEGRATION_RESULT" = "false" ]; then
    az functionapp vnet-integration add --resource-group $RESOURCE_GROUP --name $APP --vnet $AKS_CLUSTER_VNET --subnet $DELEGATED_SUBNET
fi
