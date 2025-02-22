#!/bin/sh

set -e

CODER_VERSION=$(curl -s "https://api.github.com/repos/coder/code-server/releases/latest" | jq -r .tag_name)
CODER_VERSION=${CODER_VERSION#v}
curl -fOL https://github.com/coder/code-server/releases/download/v$CODER_VERSION/code-server_${CODER_VERSION}_amd64.deb
dpkg -i code-server_${CODER_VERSION}_amd64.deb
rm code-server_${CODER_VERSION}_amd64.deb
