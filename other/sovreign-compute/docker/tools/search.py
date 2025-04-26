#!/usr/bin/python3

import os
import sys


if len(sys.argv) < 3:
    sys.exit(1)
search_extensions = sys.argv[1]
search_term = sys.argv[2]
command = f"""
vi +$(rg --line-number --no-heading --color=never $(echo '{search_extensions}' | tr ',' '\n' | sed 's/^/--glob=*./g') '{search_term}'
| exec fzf --delimiter ':' --preview 'tail -n +{{2}} {{1}}'
| awk -F: '{{ print $2, $1 }}')
"""
command = command.replace('\n', '')
os.system(f'/bin/sh -c "{command}"')
