#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

echo "--- Updating the system ---"
apt-get -yq update

echo "--- Installing utilities ---"
apt-get -yq install curl mc imagemagick python3 python3-pip python3-dev python3-tk build-essential subversion git libfreetype6-dev libpng-dev libopenblas-dev

echo "--- Installing Python modules ---"
DIRECTORY=$(dirname $0)
pip3 install --no-cache-dir --upgrade pip -r $DIRECTORY/requirements.txt

echo "--- Installing Atom editor ---"
wget -q -O /tmp/atom.deb https://atom.io/download/deb
dpkg -i /tmp/atom.deb
apt-get -yf install
