#!/bin/sh

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 PREFIX"
    echo "Example:"
    echo "$0 example"
    exit 1
else
    PREFIX=$1
fi

export RESOURCE_GROUP=${PREFIX}resources
export AKS_CLUSTER=${PREFIX}cluster

if ! command -v kubectl > /dev/null; then
    echo "Install kubectl"
    exit 1
fi
if ! command -v helm > /dev/null; then
    echo "Install helm"
    exit 1
fi
if ! command -v git > /dev/null; then
    echo "Install git"
    exit 1
fi

# Credentials for kubectl
az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER

# Install the Virtual Kubelet connector
rm -rf iot-edge-virtual-kubelet-provider 2> /dev/null
git clone https://github.com/Azure/iot-edge-virtual-kubelet-provider.git
sed -i 's/extensions\/v1beta1/apps\/v1/g' iot-edge-virtual-kubelet-provider/src/charts/iot-edge-connector/templates/deployment.yaml
cd iot-edge-virtual-kubelet-provider
helm uninstall iot-edge-connector-hub0 --namespace hub0
cd -
rm -rf iot-edge-virtual-kubelet-provider
