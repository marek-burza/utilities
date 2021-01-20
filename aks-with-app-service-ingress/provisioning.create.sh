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

sudo az aks install-cli --install-location /usr/bin/kubectl
sudo apt-get -yq install jq gettext nmap

/bin/sh $BASE/resourcegroup.create.sh $PREFIX $LOCATION

/bin/sh $BASE/storageaccount.create.sh $PREFIX $LOCATION

/bin/sh $BASE/registry.create.sh $PREFIX $LOCATION

/bin/sh $BASE/image.create.sh $PREFIX $LOCATION

/bin/sh $BASE/data.create.sh $PREFIX $LOCATION

/bin/sh $BASE/cluster.create.sh $PREFIX $LOCATION

/bin/sh $BASE/deployment.create.sh $PREFIX $LOCATION

/bin/sh $BASE/app.create.sh $PREFIX $LOCATION
