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
export IOT_HUB=${PREFIX}hub
export IOT_EDGE_DEVICE_ID=${PREFIX}prototype
export IOT_EDGE_DEPLOYMENT_ID=${PREFIX}deployment

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

export IOT_HUB_SKU=S1
export IOT_HUB_UNIT=1
export IOT_EDGE_DEPLOYMENT_PATH=${BASE}/iot_edge.deployment.json

# Make sure it is possible to use Azure IoT Edge CLI extension
az extension add --name azure-cli-iot-ext || true

# Create IoT hub if necessary
IOT_HUB_RESULT=$(az iot hub list --resource-group $RESOURCE_GROUP --query "contains([].name,'$IOT_HUB')")
if [ "$IOT_HUB_RESULT" = "false" ]; then
    az iot hub create --name $IOT_HUB --resource-group $RESOURCE_GROUP --location $LOCATION --sku $IOT_HUB_SKU --unit $IOT_HUB_UNIT
fi

# Create IoT edge device if necessary
IOT_EDGE_DEVICE_RESULT=$(az iot hub device-identity list --hub-name $IOT_HUB --query "contains([].deviceId,'$IOT_EDGE_DEVICE_ID')")
if [ "$IOT_EDGE_DEVICE_RESULT" = "false" ]; then
    az iot hub device-identity create --hub-name $IOT_HUB --device-id $IOT_EDGE_DEVICE_ID --edge-enabled true
fi
az iot hub device-identity connection-string show --hub-name $IOT_HUB --device-id $IOT_EDGE_DEVICE_ID -o tsv

# Create IoT edge deployment
IOT_EDGE_DEPLOYMENT_RESULT=$(az iot edge deployment list --hub-name $IOT_HUB --query "contains([].id,'$IOT_EDGE_DEPLOYMENT_ID')")
if [ "$IOT_EDGE_DEPLOYMENT_RESULT" = "true" ]; then
    az iot edge deployment delete --hub-name $IOT_HUB --deployment-id $IOT_EDGE_DEPLOYMENT_ID
fi
az iot edge deployment create --hub-name $IOT_HUB --deployment-id $IOT_EDGE_DEPLOYMENT_ID --content $IOT_EDGE_DEPLOYMENT_PATH --target-condition "deviceId='$IOT_EDGE_DEVICE_ID'"
