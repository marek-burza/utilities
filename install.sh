#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

echo "--- Updating the system ---"
apt-get -yq update

echo "--- Installing utilities ---"
apt-get -yq install curl mc imagemagick python3 python3-pip python3-dev python3-tk build-essential git libfreetype6-dev libpng-dev libopenblas-dev libblas-dev libatlas-base-dev

echo "--- Installing Python modules ---"
DIRECTORY=$(dirname $0)
pip3 install --upgrade pip
pip3 install --no-cache-dir -r $DIRECTORY/requirements.1.txt
pip3 install --no-cache-dir -r $DIRECTORY/requirements.2.txt
