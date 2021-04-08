#!/bin/bash

DPKG_ARCH="$(dpkg --print-architecture)"
case "${DPKG_ARCH##*-}" in
  i386)
    echo 386
    ;;
  amd64)
    echo amd64
    ;;
  armhf)
    echo arm
    ;;
  arm64)
    echo arm64
    ;;
  *)
    echo "unsupported"
    ;;
esac