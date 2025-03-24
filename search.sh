#!/bin/sh

SEARCH_EXTENSIONS=$1
SEARCH_TERM=$2

rg --line-number --no-heading --color=never $(echo "$SEARCH_EXTENSIONS" | tr ',' '\n' | sed 's/^/--glob=*./g') "$SEARCH_TERM" \
| fzf --delimiter ':' --preview 'tail -n +{2} {1}' \
| awk -F: '{ print $1, $2 }' \
| xargs nano +
