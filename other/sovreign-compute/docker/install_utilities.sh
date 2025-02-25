#!/bin/sh

set -e

apt-get update -yq
apt-get install -yq \
  build-essential \
  curl \
  git \
  jq \
  nano \
  procps \
  sudo \
  supervisor \
  tmux \
  vim
