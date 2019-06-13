#!/bin/sh

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: ./service.create.sh PREFIX LOCATION"
    echo "Example:"
    echo "./service.create.sh example centralus"
    exit 1
else
    PREFIX=$1
    LOCATION=$2
fi


export RESOURCE_GROUP=${PREFIX}resourcegroup
export STORAGE_ACCOUNT=${PREFIX}storageaccount
export CONTAINER_NAME=${PREFIX}container
export APP=${PREFIX}app
export AD_NAME=${PREFIX}ad

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if ! command -v envsubst > /dev/null; then
    echo "Install gettext package"
    exit 1
fi

# az login
# Create the resource group
az group create --name $RESOURCE_GROUP --location $LOCATION
# Create the storage account
az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS
# Create the function app
az functionapp create --name $APP --consumption-plan-location $LOCATION --resource-group $RESOURCE_GROUP --storage-account $STORAGE_ACCOUNT
rm function.zip 2> /dev/null || true
mkdir -p $BASE/.azurefunctions/swagger
envsubst '$APP' < $BASE/swagger.json.template > $BASE/.azurefunctions/swagger/swagger.json
envsubst '$STORAGE_ACCOUNT$CONTAINER_NAME' < $BASE/proxies.json.template > $BASE/proxies.json
zip -r function.zip host.json proxies.json .azurefunctions generate
az functionapp deployment source config-zip --resource-group $RESOURCE_GROUP --name $APP --src function.zip
az functionapp config appsettings set --name $APP --resource-group $RESOURCE_GROUP --settings ENVIRONMENT_VARIABLE=VALUE
# Create static content container and upload content
curl -L https://unpkg.com/swagger-client@3.8.25/browser/index.js -o $BASE/swagger-client.js
az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --public-access blob
az storage blob upload --file $BASE/index.html --container-name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --name index.html
az storage blob upload --file $BASE/.azurefunctions/swagger/swagger.json --container-name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --name swagger-original.json
az storage blob upload --file $BASE/swagger-client.js --container-name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --name swagger-client.js
# Add Authentication / Authorization to the function app
PASSWORD=$(openssl rand -base64 32)
AAD_ID=$(az ad app create --display-name $AD_NAME --native-app false --password $PASSWORD --end-date $(date --date='10 years' +"%Y-%m-%d") --homepage https://$APP.azurewebsites.net --identifier-uris https://$APP.azurewebsites.net --reply-urls https://$APP.azurewebsites.net/.auth/login/aad/callback --required-resource-accesses @manifest.sign_in_and_read_user_profile.json --query ["appId"][0] --output tsv)
AAD_URL=$(az cloud show --query ["endpoints.activeDirectory"][0] --output tsv)
TENNANT_ID=$(az account show --query ["tenantId"][0] --output tsv)
TOKEN_ISSUER=$(curl -s $AAD_URL/$TENNANT_ID/.well-known/openid-configuration | jq -r '.issuer')
az webapp auth update \
  --resource-group $RESOURCE_GROUP \
  --name $APP \
  --enabled true \
  --action LoginWithAzureActiveDirectory \
  --aad-allowed-token-audiences https://$APP.azurewebsites.net/.auth/login/aad/callback \
  --aad-client-id $AAD_ID \
  --aad-client-secret "$PASSWORD" \
  --aad-token-issuer-url $TOKEN_ISSUER
# Clean-up
rm -rf $BASE/.azurefunctions || true
rm $BASE/proxies.json $BASE/function.zip $BASE/swagger-client.js || true
