#!/bin/sh

set -e

apt-get update -yq
apt-get install -yq sudo

USER=user
echo "$USER ALL=(ALL) NOPASSWD: ALL" > /etc/sudoers.d/$USER
chmod 0440 /etc/sudoers.d/$USER
