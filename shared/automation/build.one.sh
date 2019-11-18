#!/bin/sh

set -e

IMAGE=$(basename $(dirname $1))

docker build -f $1 -t $IMAGE .
