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

# Make sure it is possible to use Azure IoT Edge CLI extension
az extension add --name azure-cli-iot-ext || true

# Create IoT edge deployment
IOT_EDGE_DEPLOYMENT_RESULT=$(az iot edge deployment list --hub-name $IOT_HUB --query "contains([].id,'$IOT_EDGE_DEPLOYMENT_ID')")
if [ "$IOT_EDGE_DEPLOYMENT_RESULT" = "true" ]; then
    az iot edge deployment delete --hub-name $IOT_HUB --deployment-id $IOT_EDGE_DEPLOYMENT_ID
fi

# Destroy IoT edge device
IOT_EDGE_DEVICE_RESULT=$(az iot hub device-identity list --hub-name $IOT_HUB --query "contains([].deviceId,'$IOT_EDGE_DEVICE_ID')")
if [ "$IOT_EDGE_DEVICE_RESULT" = "true" ]; then
    az iot hub device-identity delete --hub-name $IOT_HUB --device-id $IOT_EDGE_DEVICE_ID
fi

# Destroy IoT hub
IOT_HUB_RESULT=$(az iot hub list --resource-group $RESOURCE_GROUP --query "contains([].name,'$IOT_HUB')")
if [ "$IOT_HUB_RESULT" = "true" ]; then
    az iot hub delete --name $IOT_HUB --resource-group $RESOURCE_GROUP
fi
