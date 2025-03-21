#!/bin/sh

set -e

apt-get update -yq
apt-get install -yq \
  build-essential \
  curl \
  git \
  imagemagick \
  jq \
  nano \
  poppler-tools \
  procps \
  qpdf \
  sudo \
  supervisor \
  tmux \
  vim
