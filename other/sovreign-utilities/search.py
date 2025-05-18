#!/usr/bin/python3

import os
import sys


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(1)
    search_extensions = ' '.join([f'--glob=*.{extension}' for extension in sys.argv[1].split(',')])
    search_term = sys.argv[2]
    command = f"""
    vi +$(rg --line-number --no-heading --color=never {search_extensions} '{search_term}'
    | exec fzf --delimiter ':' --preview 'tail -n +{{2}} {{1}}'
    | awk -F: '{{ print $2, $1 }}')
    """
    command = command.replace('\n', '')
    os.system(f'/bin/sh -c "{command}"')
