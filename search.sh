#!/bin/bash

EXTENSIONS=$1
PATTERN=$2

GLOBS=$(for extension in ${EXTENSIONS//,/ }; do echo -n " --glob '*.$extension'"; done)

SELECTION=$(eval rg --line-number --no-heading --color=never $GLOBS "'"$PATTERN"'" . \
    | fzf --delimiter ':' --preview 'tail -n +{2} {1}' \
    | awk -F: '{ print $1, $2 }' \
    | nano +$1 $0)

echo $SELECTION
