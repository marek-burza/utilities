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

/bin/sh $BASE/deployment.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/app.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/files.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/service.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/registry.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/storageaccount.destroy.sh $PREFIX $LOCATION

/bin/sh $BASE/resourcegroup.destroy.sh $PREFIX $LOCATION
