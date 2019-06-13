#!/bin/sh

# Check input arguments
if [ "$#" -ne 8 ]; then
    echo "Usage: ./iot_edge.creation.sh RESOURCE_GROUP LOCATION IOT_HUB IOT_HUB_SKU IOT_HUB_UNIT IOT_EDGE_DEVICE_ID IOT_EDGE_DEPLOYMENT_ID IOT_EDGE_DEPLOYMENT_PATH"
    echo "Arguments:"
    echo "    RESOURCE_GROUP           - Name of the resource group"
    echo "    LOCATION                 - Location for the resources"
    echo "    IOT_HUB                  - Name of the IoT hub"
    echo "    IOT_HUB_SKU              - SKU of the IoT hub"
    echo "    IOT_HUB_UNIT             - Unit count of the IoT hub"
    echo "    IOT_EDGE_DEVICE_ID       - Name of the IoT edge device"
    echo "    IOT_EDGE_DEPLOYMENT_ID   - Name of the IoT edge deployment"
    echo "    IOT_EDGE_DEPLOYMENT_PATH - Path to the IoT edge deployment config"
    echo "Example:"
    echo "./iot_edge.creation.sh exampleresources northeurope examplehub F1 1 exampledevice exampledeployment ./iot_edge.deployment.json"
    exit 1
else
    RESOURCE_GROUP=$1
    LOCATION=$2
    IOT_HUB=$3
    IOT_HUB_SKU=$4
    IOT_HUB_UNIT=$5
    IOT_EDGE_DEVICE_ID=$6
    IOT_EDGE_DEPLOYMENT_ID=$7
    IOT_EDGE_DEPLOYMENT_PATH=$8
fi

# Log in
az login --service-principal -u $AZURE_USER -p $AZURE_PASSWORD --tenant $AZURE_TENANT || exit

# Make sure it is possible to use Azure IoT Edge CLI extension
az extension add --name azure-cli-iot-ext || true

# Create resource group if necessary
RESOURCE_GROUP_RESULT=$(az group exists --name $RESOURCE_GROUP)
if [ "$RESOURCE_GROUP_RESULT" != "true" ]; then
  az group create --location $LOCATION --name $RESOURCE_GROUP
fi

# Create IoT hub if necessary
az iot hub show --name $IOT_HUB --resource-group $RESOURCE_GROUP
IOT_HUB_RESULT=$?
if [ "$IOT_HUB_RESULT" != "0" ]; then
  az iot hub create --name $IOT_HUB --resource-group $RESOURCE_GROUP --location $LOCATION --sku $IOT_HUB_SKU --unit $IOT_HUB_UNIT
fi

# Create IoT edge device if necessary
az iot hub device-identity show --hub-name $IOT_HUB --device-id $IOT_EDGE_DEVICE_ID
IOT_EDGE_DEVICE_RESULT=$?
if [ "$IOT_EDGE_DEVICE_RESULT" != "0" ]; then
  az iot hub device-identity create --hub-name $IOT_HUB --device-id $IOT_EDGE_DEVICE_ID --edge-enabled true
fi
az iot hub device-identity show-connection-string --hub-name $IOT_HUB --device-id $IOT_EDGE_DEVICE_ID

# Create IoT edge deployment
az iot edge deployment show --hub-name $IOT_HUB --deployment-id $IOT_EDGE_DEPLOYMENT_ID
IOT_EDGE_DEPLOYMENT_RESULT=$?
if [ "$IOT_EDGE_DEPLOYMENT_RESULT" == "0" ]; then
  az iot edge deployment delete --hub-name $IOT_HUB --deployment-id $IOT_EDGE_DEPLOYMENT_ID
fi
az iot edge deployment create --hub-name $IOT_HUB --deployment-id $IOT_EDGE_DEPLOYMENT_ID --content $IOT_EDGE_DEPLOYMENT_PATH --target-condition "deviceId='$IOT_EDGE_DEVICE_ID'"
