#!/usr/bin/env -S uv run --script --quiet

import os
import subprocess
import sys

def main():
    HOME = os.environ['HOME']
    for cmd in [
        ['claude', 'plugin', 'marketplace', 'add', 'huggingface/skills'],
        ['claude', 'plugin', 'install', 'huggingface-best@huggingface-skills', '--scope', 'user'],
        ['claude', 'plugin', 'update', 'huggingface-best@huggingface-skills', '--scope', 'user'],
        ['mkdir', '-p', f'{HOME}/.config/opencode/skills/huggingface-best'],
        ['curl', '-sSL', '-o', f'{HOME}/.config/opencode/skills/huggingface-best/SKILL.md',
         'https://raw.githubusercontent.com/huggingface/skills/main/skills/huggingface-best/SKILL.md'],
    ]:
        result = subprocess.run(cmd, text=True)
        if result.returncode != 0:
            sys.exit(result.returncode)


if __name__ == '__main__':
    main()
