#!/bin/sh

set -e

apt-get update -yq
apt-get install -yq \
  build-essential \
  curl \
  git \
  jq \
  procps \
  sudo \
  supervisor
