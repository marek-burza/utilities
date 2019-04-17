#!/bin/sh

set -e

export DEBIAN_FRONTEND=noninteractive
export CODENAME=$(. /etc/os-release && echo $VERSION_CODENAME)
export APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=1

echo "--- Updating the system ---"
apt-get -yq update

echo "--- Installing utilities ---"
apt-get -yq install apt-transport-https ca-certificates software-properties-common command-not-found curl zip nano mc imagemagick ffmpeg poppler-utils libgxps-utils python3 python3-pip python3-dev python3-tk build-essential git libfreetype6-dev libpng-dev libopenblas-dev libblas-dev libatlas-base-dev jq mosquitto mosquitto-dev mosquitto-clients ntpdate
sed -i '/PDF/d' /etc/ImageMagick-6/policy.xml
ntpdate 0.pool.ntp.org

echo "--- Installing Docker ---"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
echo "deb [arch=amd64] https://download.docker.com/linux/ubuntu $CODENAME stable" | tee /etc/apt/sources.list.d/docker-ce.list
apt-get -yq update
apt-get -yq install docker-ce
if [ "$#" -eq 1 ]; then
    groupadd docker 2> /dev/null || true
    /bin/sh -c "usermod -aG docker $1"
fi

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
