#!/bin/sh

set -e

apt-get update -yq
apt-get install -yq \
  curl \
  build-essential \
  git \
  jq \
  sudo \
  supervisor
