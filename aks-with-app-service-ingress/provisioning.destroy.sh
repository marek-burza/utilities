#!/bin/sh

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 PREFIX LOCATION"
    echo "Example:"
    echo "$0 example centralus"
    exit 1
else
    PREFIX=$1
    LOCATION=$2
fi

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

if [ -z "${EXAMPLE_VARIABLE}" ]; then
    echo "Error: EXAMPLE_VARIABLE must be defined"
    exit 1
fi

sudo az aks install-cli --install-location /usr/bin/kubectl
sudo apt-get -yq install jq gettext nmap

/bin/sh $BASE/app.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/deployment.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/cluster.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/data.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/image.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/registry.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/storageaccount.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/resourcegroup.destroy.sh $PREFIX $LOCATION
