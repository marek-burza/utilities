#!/bin/sh
# Inspired by https://github.com/WAGO/azure-iot-edge

CONFIG_YAML=$(cat /etc/iotedge/config.yaml)
[ -z "$CONFIG_YAML" ] && cp /etc/iotedge/config.yaml.template /etc/iotedge/config.yaml

if cmp -s /etc/iotedge/config.yaml.template /etc/iotedge/config.yaml; then
  cat /etc/iotedge/config.yaml.template | sed '/^[[:blank:]]*#/d;s/#.*//' | grep -v "^$" > /etc/iotedge/config.yaml.compact
  cp /etc/iotedge/config.yaml.compact /etc/iotedge/config.yaml
fi

cat /etc/iotedge/config.yaml | \
yq w - moby_runtime.docker_uri '/var/run/docker.sock' | \
yq d - moby_runtime.uri > /etc/iotedge/config.yaml.docker
cp /etc/iotedge/config.yaml.docker /etc/iotedge/config.yaml

cat /etc/iotedge/config.yaml | \
yq w - hostname $HOSTNAME > /etc/iotedge/config.yaml.hostname
cp /etc/iotedge/config.yaml.hostname /etc/iotedge/config.yaml

NETWORK=$(yq r /etc/iotedge/config.yaml moby_runtime.network.name)
[ -z "$NETWORK" ] && NETWORK=$(yq r /etc/iotedge/config.yaml moby_runtime.network | grep -v ':')
[ -z "$NETWORK" ] && NETWORK="azure-iot-edge"
docker network create $NETWORK 2> /dev/null
docker network connect $NETWORK $HOSTNAME 2> /dev/null
HOST_IP=$(docker inspect $HOSTNAME | yq r - '.NetworkSettings.Networks."'$NETWORK'".IPAddress')
cat /etc/iotedge/config.yaml | \
yq w - connect.management_uri 'http://'$HOST_IP':15580/' | \
yq w - connect.workload_uri 'http://'$HOST_IP':15581/' | \
yq w - listen.management_uri 'http://'$HOST_IP':15580/' | \
yq w - listen.workload_uri 'http://'$HOST_IP':15581/' > /etc/iotedge/config.yaml.uris
cp /etc/iotedge/config.yaml.uris /etc/iotedge/config.yaml

if [ ! -z "$AZURE_IOT_EDGE_CONNECTION_STRING" ]; then
  cat /etc/iotedge/config.yaml | \
  yq w - provisioning.device_connection_string $AZURE_IOT_EDGE_CONNECTION_STRING > /etc/iotedge/config.yaml.credentials
  cp /etc/iotedge/config.yaml.credentials /etc/iotedge/config.yaml
fi

cat /etc/iotedge/config.yaml
exec /usr/bin/iotedged -c /etc/iotedge/config.yaml
