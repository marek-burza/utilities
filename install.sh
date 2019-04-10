#!/bin/sh

set -e

export DEBIAN_FRONTEND=noninteractive
export CODENAME=$(. /etc/os-release && echo $VERSION_CODENAME)
export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

if [ $(id -u) = 0 ]; then
    export SUDO=
else
    export SUDO=sudo
fi

echo "--- Updating the system ---"
$SUDO apt-get -yq update

echo "--- Installing utilities ---"
$SUDO apt-get -yq install apt-transport-https ca-certificates software-properties-common command-not-found curl zip nano mc imagemagick ffmpeg poppler-utils libgxps-utils python3 python3-pip python3-dev python3-tk build-essential git libfreetype6-dev libpng-dev libopenblas-dev libblas-dev libatlas-base-dev jq mosquitto mosquitto-dev mosquitto-clients
$SUDO sed -i '/PDF/d' /etc/ImageMagick-6/policy.xml

echo "--- Installing Docker ---"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | $SUDO apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable" | $SUDO tee /etc/apt/sources.list.d/docker-ce.list
$SUDO apt-get -yq update
$SUDO apt-get -yq install docker-ce
if ! [ $(id -u) = 0 ]; then
    $SUDO groupadd docker 2> /dev/null || true
    /bin/sh -c "$SUDO usermod -aG docker $USER"
fi

echo "--- Installing Azure CLI ---"
echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $CODENAME main" | $SUDO tee /etc/apt/sources.list.d/azure-cli.list
curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | $SUDO apt-key add -
$SUDO apt-get -yq update
$SUDO apt-get -yq install azure-cli

echo "--- Installing Python modules ---"
DIRECTORY=$(dirname $0)
$SUDO pip3 install --no-cache-dir -r $DIRECTORY/requirements.txt

echo "--- Clean-up ---"
$SUDO apt-get -yq autoremove
