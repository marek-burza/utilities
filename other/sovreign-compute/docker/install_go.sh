#!/bin/sh

set -e

GO_VERSION=$(curl -sL https://golang.org/dl/ | grep -oP 'go[0-9]+\.[0-9]+\.[0-9]+' | sort -V | tail -n 1)
curl -sSLO https://go.dev/dl/${GO_VERSION}.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf ${GO_VERSION}.linux-amd64.tar.gz
