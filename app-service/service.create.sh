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
export FILES_SHARE_NAME=${PREFIX}share
export VOLUME_NAME=${PREFIX}volume
export CONSUMPTION_PLAN=${PREFIX}consumptionplan
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
RESOURCE_GROUP_RESULT=$(az group exists --name $RESOURCE_GROUP)
if [ "$RESOURCE_GROUP_RESULT" = "false" ]; then
    az group create --name $RESOURCE_GROUP --location $LOCATION
fi
# Create the storage account
STORAGE_ACCOUNT_RESULT=$(az storage account check-name --name $STORAGE_ACCOUNT --query nameAvailable)
if [ "$STORAGE_ACCOUNT_RESULT" = "true" ]; then
    az storage account create --name $STORAGE_ACCOUNT --location $LOCATION --resource-group $RESOURCE_GROUP --sku Standard_LRS
fi
STORAGE_ACCOUNT_CONNECTION_STRING=$(az storage account show-connection-string --resource-group $RESOURCE_GROUP --name $STORAGE_ACCOUNT -o tsv)
# Create the static content container and upload content
CONTAINER_RESULT=$(az storage container list --account-name $STORAGE_ACCOUNT --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING --query "contains([].name, '$CONTAINER_NAME')")
if [ "$CONTAINER_RESULT" = "false" ]; then
    az storage container create --name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --public-access off --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
fi
envsubst '$APP' < $BASE/swagger.json.template > $BASE/wwwroot/swagger.json
curl -L https://unpkg.com/swagger-client@3.8.25/browser/index.js -o $BASE/wwwroot/swagger-client.js
export ENTRIES
EXPIRY=$(date --date='10 years' '+%Y-%m-%dT%H:%MZ')
cd $BASE/wwwroot/
for FILE in $(find . -type f | cut -c 3-)
do
    export FILE
    az storage blob upload --file $FILE --container-name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --name $FILE --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
    export URL=https://$STORAGE_ACCOUNT.blob.core.windows.net/$CONTAINER_NAME/$FILE?$(az storage blob generate-sas --container-name $CONTAINER_NAME --account-name $STORAGE_ACCOUNT --name $FILE --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING --permissions r --expiry $EXPIRY --https-only --output tsv)
    ENTRY=$(envsubst '\$FILE\$URL' < $BASE/proxies-entry.json.template)
    ENTRIES=$ENTRIES$ENTRY
done
cd -
# Create the files volume and upload content
FILES_SHARE_RESULT=$(az storage share list --account-name $STORAGE_ACCOUNT --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING --query "contains([].name, '$FILES_SHARE_NAME')")
if [ "$FILES_SHARE_RESULT" = "false" ]; then
  az storage share create --name $FILES_SHARE_NAME --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
fi
date > $BASE/date.txt
az storage file upload --source $BASE/date.txt --share-name $FILES_SHARE_NAME --account-name $STORAGE_ACCOUNT --connection-string $STORAGE_ACCOUNT_CONNECTION_STRING
# Create the consumption plan
CONSUMPTION_PLAN_RESULT=$(az functionapp plan list --query "contains([].name, '$CONSUMPTION_PLAN')")
if [ "$CONSUMPTION_PLAN_RESULT" = "false" ]; then
    az functionapp plan create --resource-group $RESOURCE_GROUP --name $CONSUMPTION_PLAN --sku B1 --is-linux true
fi
# Create the function app
APP_RESULT=$(az functionapp list --resource-group $RESOURCE_GROUP --query "contains([].name,'$APP')")
if [ "$APP_RESULT" = "false" ]; then
    az functionapp create --name $APP --plan $CONSUMPTION_PLAN --resource-group $RESOURCE_GROUP --storage-account $STORAGE_ACCOUNT --os-type Linux --runtime python --runtime-version 3.7 --functions-version 2
fi
rm -rf $BASE/app/.python_packages 2> /dev/null || true
rm -rf $BASE/app/azure-functions-core-tools 2> /dev/null || true
while [ $(az functionapp list --query "contains([?state=='Running'].name, '$APP')") = "false" ]; do
    echo "Waiting..."
    sleep 5
done
envsubst '$ENTRIES$APP' < $BASE/proxies.json.template > $BASE/app/proxies.json
cat $BASE/app/proxies.json
cd $BASE/app
until func azure functionapp publish $APP --python
do
    echo "Waiting..."
    sleep 5
done
cd -
# Create the AD client
AAD_ID=$(az ad app list --query "[?displayName == '$AD_NAME'].appId" --all --output tsv)
if [ "$AAD_ID" = "" ]; then
    PASSWORD=$(openssl rand -base64 32)
    az ad app create --display-name $AD_NAME --password $PASSWORD --end-date $(date --date='10 years' +"%Y-%m-%d") --native-app false --homepage https://$APP.azurewebsites.net --identifier-uris https://$APP.azurewebsites.net --reply-urls https://$APP.azurewebsites.net/.auth/login/aad/callback --required-resource-accesses @manifest.sign_in_and_read_user_profile.json
fi
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
# Configure auth refresh (works only for a web app but web app does not have proxies)
# RESOURCE_ID=$(az resource show --resource-group $RESOURCE_GROUP --resource-type Microsoft.Web/sites --name $APP --query id --output tsv)/config/authsettings
# RESOURCE_PROPERTIES='{"additionalLoginParams": ["response_type=code id_token", "resource='$AAD_ID'"]}'
# az resource invoke-action --action list --ids $RESOURCE_ID
# az resource create --id $RESOURCE_ID --properties "$RESOURCE_PROPERTIES"
# Add the Volume
VOLUME_RESULT=$(az webapp config storage-account list --resource-group $RESOURCE_GROUP --name $APP --query "contains([].name, '$VOLUME_NAME')")
if [ "$VOLUME_RESULT" = "false" ]; then
    STORAGE_KEY=$(az storage account keys list --resource-group $RESOURCE_GROUP --account-name $STORAGE_ACCOUNT --query "[0].value" -o tsv)
    az webapp config storage-account add --resource-group $RESOURCE_GROUP --name $APP --custom-id $VOLUME_NAME --storage-type AzureFiles --account-name $STORAGE_ACCOUNT --share-name $FILES_SHARE_NAME --access-key "$STORAGE_KEY" --mount-path "/data"
fi
# Clean-up
rm $BASE/app/proxies.json 2> /dev/null || true
rm $BASE/wwwroot/swagger.json 2> /dev/null || true
rm $BASE/wwwroot/swagger-client.js 2> /dev/null || true
rm $BASE/date.txt 2> /dev/null || true
rm -rf $BASE/app/.python_packages 2> /dev/null || true
rm -rf $BASE/app/azure-functions-core-tools 2> /dev/null || true
