#!/bin/bash

set -e

echo -n "Password: "
read -s PASSWORD1
echo ""
echo -n "Password (repeat): "
read -s PASSWORD2
echo ""
if [ "$PASSWORD1" == "$PASSWORD2" ]; then
    mv $1 _$1
    qpdf --encrypt $PASSWORD $PASSWORD 256 -- $1 _$1
fi
