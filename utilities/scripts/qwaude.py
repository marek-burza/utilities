#!/usr/bin/env -S uv run --script --quiet

import os


if __name__ == '__main__':
    os.environ['ANTHROPIC_AUTH_TOKEN'] = 'ollama'
    os.environ['ANTHROPIC_API_KEY'] = ''
    os.environ['ANTHROPIC_BASE_URL'] = 'http://host.docker.internal:11434'
    os.system('claude --model qwen3.5:35b')
