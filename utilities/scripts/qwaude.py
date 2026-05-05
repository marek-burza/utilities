#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
# ]
# ///

import os

import typer


def main(
    model: str = typer.Option(
        'qwen3.5:35b',
        '--model',
        help='Model name to pass to coding agent.',
    ),
) -> None:
    os.environ['ANTHROPIC_AUTH_TOKEN'] = 'ollama'
    os.environ['ANTHROPIC_API_KEY'] = ''
    os.environ['ANTHROPIC_BASE_URL'] = 'http://host.docker.internal:11434'
    os.system(f'claude --model {model}')


if __name__ == '__main__':
    typer.run(main)
