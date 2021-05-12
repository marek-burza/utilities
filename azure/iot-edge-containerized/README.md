# Containerized Azure IoT Edge

To run it:

    docker run --name azure-iot-edge --restart=always -d -v /var/run/docker.sock:/var/run/docker.sock -v $PWD/config.yaml:/etc/iotedge/config.yaml -e AZURE_IOT_EDGE_CONNECTION_STRING="$AZURE_IOT_EDGE_CONNECTION_STRING" altermarkive/azure-iot-edge
