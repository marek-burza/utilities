#!/bin/sh

set -e

export DEBIAN_FRONTEND=noninteractive
export CODENAME=$(. /etc/os-release && echo $VERSION_CODENAME)
export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

echo "--- Updating the system ---"
apt-get -yq update

echo "--- Installing utilities ---"
apt-get -yq install apt-transport-https ca-certificates gnupg-agent software-properties-common curl zip python3 python3-pip python3-dev

echo "--- Installing Azure CLI ---"
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $CODENAME main" | tee /etc/apt/sources.list.d/azure-cli.list
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
apt-get -yq update
apt-get -yq install azure-cli

echo "--- Installing Python modules ---"
DIRECTORY=$(dirname $0)
pip3 install --no-cache-dir -r $DIRECTORY/requirements.txt

echo "--- Clean-up ---"
apt-get -yq autoremove
