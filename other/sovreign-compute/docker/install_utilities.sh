#!/bin/sh

set -e

apt-get update -yq
apt-get install -yq \
  build-essential \
  curl \
  fzf \
  git \
  imagemagick \
  jq \
  nano \
  poppler-utils \
  procps \
  qpdf \
  ripgrep \
  sudo \
  supervisor \
  tmux \
  vim
