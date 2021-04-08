#!/bin/bash

DPKG_ARCH="$(dpkg --print-architecture)"
case "${DPKG_ARCH##*-}" in
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