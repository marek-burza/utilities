# Introduction

This repository contains the code of an example Azure IoT Edge module - it demonstrates the boilerplate code for the module itself as well as the service.


# Preconditions

To install the IoT Edge CLI extension run the following command:

    az extension add --name azure-cli-iot-ext

You must already have an Azure IoT Hub and Azure IoT Edge Device resources created.


# Running the code

To build and push the Docker container image of the Azure IoT Edge module the following environment variables must be set:

* `IOTEDGE_MODULE_IMAGE_URI`

To build and push the Docker container image of the Azure IoT Edge module run the following commands:

    docker build -t $IOTEDGE_MODULE_IMAGE_URI .
    docker push $IOTEDGE_MODULE_IMAGE_URI

To create a Azure IoT Edge module deployment the following environment variables must be set:

* `IOTHUB_NAME`
* `IOTEDGE_DEPLOYMENT_ID`
* `IOTEDGE_DEVICE_ID`
* `IOTEDGE_MODULE_NAME`
* `IOTEDGE_MODULE_IMAGE_URI`

To create a Azure IoT Edge module deployment run the following commands:

    envsubst '$IOTEDGE_MODULE_NAME$IOTEDGE_MODULE_IMAGE_URI' < iot-edge-deployment.json.template > iot-edge-deployment.json
    az iot edge deployment create --hub-name $IOTHUB_NAME --deployment-id $IOTEDGE_DEPLOYMENT_ID --content iot-edge-deployment.json --target-condition "deviceId='$IOTEDGE_DEVICE_ID'"

To adjust the value in the module twin the following environment variables must be set:

* `IOTHUB_SERVICE_CONNECTION_STRING`
* `IOTEDGE_DEVICE_ID`
* `IOTEDGE_MODULE_NAME`
* `IOTEDGE_MODULE_IMAGE_URI`

To adjust the value in the module twin run the following command:

    docker run --rm -it -e IOTHUB_SERVICE_CONNECTION_STRING=$IOTHUB_SERVICE_CONNECTION_STRING -e IOTEDGE_DEVICE_ID=$IOTEDGE_DEVICE_ID -e IOTEDGE_MODULE_NAME=$IOTEDGE_MODULE_NAME $IOTEDGE_MODULE_IMAGE_URI "$RANDOM"

This will result in the following (Docker) log entry of the module:

    info: module.Program[0]
          Desired property change: {"value":8498,"$version":2}
    info: module.Program[0]
          Sending current value as reported property

To find the connection string (for the `IOTHUB_SERVICE_CONNECTION_STRING` variable) follow this path on the Azure portal:

    Iot Hub -> [Your IoT Hub Instance] -> Shared access policies -> service -> Connection string—primary key


# Other materials

Cross-compiled Docker containers: [https://docs.resin.io/reference/base-images/resin-base-images/#resin-xbuild-qemu](https://docs.resin.io/reference/base-images/resin-base-images/#resin-xbuild-qemu)
