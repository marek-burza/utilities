#!/bin/sh

set -e

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 PREFIX LOCATION"
    exit 1
else
    PREFIX=$1
    LOCATION=$2
fi

SELF=$0
REAL=$(realpath "$SELF")
BASE=$(dirname "$REAL")

apt-get -yq install jq gettext

/bin/sh $BASE/resourcegroup.create.sh $PREFIX $LOCATION

/bin/sh $BASE/storageaccount.create.sh $PREFIX $LOCATION

/bin/sh $BASE/registry.create.sh $PREFIX $LOCATION

/bin/sh $BASE/service.create.sh $PREFIX $LOCATION

/bin/sh $BASE/files.create.sh $PREFIX $LOCATION

/bin/sh $BASE/app.create.sh $PREFIX $LOCATION

/bin/sh $BASE/deployment.create.sh $PREFIX $LOCATION
