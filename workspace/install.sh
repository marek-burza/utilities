#!/bin/sh

set -e

export DEBIAN_FRONTEND=noninteractive
export CODENAME=$(. /etc/os-release && echo $VERSION_CODENAME)
export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

echo "--- Updating the system ---"
apt-get -yq update

echo "--- Installing utilities ---"
apt-get -yq install apt-transport-https ca-certificates gnupg-agent software-properties-common curl zip python3 python3-pip python3-dev python3-tk build-essential git libfreetype6-dev libpng-dev gettext nmap netcat-openbsd tcpdump

echo "--- Installing Azure CLI ---"
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $CODENAME main" | tee /etc/apt/sources.list.d/azure-cli.list
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
apt-get -yq update
apt-get -yq install azure-cli

echo "--- Installing Python modules ---"
DIRECTORY=$(dirname $0)
pip3 install --no-cache-dir -r $DIRECTORY/requirements.txt

echo "--- Installing date/time enforcement ---"

git clone --branch v0.9.8 https://github.com/wolfcw/libfaketime.git /tmp/libfaketime
cd /tmp/libfaketime
make install
cd -
rm -rf /tmp/libfaketime
echo "Example use:"
echo "  LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1 FAKETIME_NO_CACHE=1 FAKETIME='1970-01-01 00:00:00' date"
echo "  LD_PRELOAD=/usr/local/lib/faketime/libfaketime.so.1 FAKETIME_NO_CACHE=1 FAKETIME='+365d' date"

echo "--- Clean-up ---"
apt-get -yq autoremove
