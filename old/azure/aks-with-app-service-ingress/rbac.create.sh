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

export SERVICE_PRINCIPAL=${PREFIX}automation

# Create the service principal
SERVICE_PRINCIPAL_RESULT=$(az ad sp list --show-mine --query "contains([].appDisplayName, '$SERVICE_PRINCIPAL')")
if [ "$SERVICE_PRINCIPAL_RESULT" = "false" ]; then
    az ad sp create-for-rbac --name http://$SERVICE_PRINCIPAL --skip-assignment --sdk-auth
fi
