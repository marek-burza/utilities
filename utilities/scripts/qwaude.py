#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "psutil",
#     "typer",
# ]
# ///

import os
import re
import subprocess
import threading
import json
from pathlib import Path

import typer
from psutil import cpu_count


LLAMA_SERVER_PORT = 8080
LLAMA_SERVER_URL = f'http://127.0.0.1:{LLAMA_SERVER_PORT}'
LLAMA_SERVER_EXTRA_PARAMS: dict[str, list[str]] = {
    'unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL': [
        '-ngl', '99',
        '-c', '131072',
        '-fa', 'on',
        '-np', '1',
        '--no-context-shift',
        '--cache-type-k', 'q4_0',  # Try q8_0 but might need to reduce context size
        '--cache-type-v', 'q4_0',
        '--jinja',  # Correct chat-template / reasoning handling
        '--reasoning', 'on',
        '--reasoning-budget', '2048',  # Caps thinking, anti-loop guard
        '--temp', '0.6',
        '--top-p', '0.95',
        '--top-k', '20',
        '--min-p', '0',
        '--presence-penalty', '1.1',  # Primary anti-looping lever
        '-b', '4096',  # Batch tuning (max number of tokens llama.cpp accepts into one processing call)
        '-ub', '2048',  # Ubatch tuning (how many tokens are actually computed together in a single GPU pass, and the one that grows your VRAM compute buffer)
        '--threads', str(cpu_count(logical=False)),
        '--no-mmproj',
    ],
    'unsloth/Qwen3.6-27B-MTP-GGUF:Q8_0': [
        '-ngl', '99',
        '-c', '131072',  # 65536?
        '-fa', 'on',
        '--no-context-shift',
        '--cache-type-k', 'q8_0',
        '--cache-type-v', 'q8_0',
        '--jinja',  # Correct chat-template / reasoning handling
        '--spec-type', 'draft-mtp',
        '--reasoning', 'on',
        '--reasoning-budget', '2048',  # Caps thinking, anti-loop guard
        '--temp', '0.6',
        '--top-p', '0.95',
        '--top-k', '20',
        '--min-p', '0',
        '--presence-penalty', '1.1',  # Primary anti-looping lever
        '-b', '4096',  # Batch tuning (max number of tokens llama.cpp accepts into one processing call)
        '-ub', '2048',  # Ubatch tuning (how many tokens are actually computed together in a single GPU pass, and the one that grows your VRAM compute buffer)
        '--threads', str(cpu_count(logical=False)),
        '--no-mmproj',
    ],
}
DEFAULT_MODEL = 'unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL'


def llama_server_download(model_uri: str) -> None:
    with subprocess.Popen(['llama-cli', '-hf', model_uri, '-n', '0'], stdin=subprocess.PIPE, text=True) as process:
        process.stdin.write('/exit\n')
        process.stdin.close()
        process.wait()


def ensure_opencode_config(model: str, web: bool) -> None:
    config_dir = Path('~/.config/opencode').expanduser()
    config_path = config_dir / 'opencode.json'
    config_dir.mkdir(parents=True, exist_ok=True)
    models = {}
    for uri in LLAMA_SERVER_EXTRA_PARAMS:
        models[uri] = {
            'name': uri,
            'tool_call': True,
            'attachment': True,
            'reasoning': True,
        }
    config = {
        '$schema': 'https://opencode.ai/config.json',
        'provider': {
            'llama.cpp': {
                'npm': '@ai-sdk/openai-compatible',
                'name': 'llama.cpp',
                'options': {
                    'baseURL': f'{LLAMA_SERVER_URL}/v1',
                },
                'models': models,
            },
        },
        'model': f'llama.cpp/{model}',
    }
    if web:
        config['server'] = {'port': 4096}
    with config_path.open('w') as handle:
        json.dump(config, handle, indent=2)


def ensure_attribution_header_disabled() -> None:
    settings_path = Path('~/.claude/settings.json').expanduser()
    settings = {}
    if settings_path.exists():
        try:
            with settings_path.open('r') as f:
                settings = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass

    settings.setdefault('env', {}).update({'CLAUDE_CODE_ATTRIBUTION_HEADER': '0'})
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    with settings_path.open('w') as f:
        json.dump(settings, f, indent=2)


def llama_server_worker(model_uri: str, exit: threading.Event) -> None:
    extra = LLAMA_SERVER_EXTRA_PARAMS.get(model_uri, [])
    cmd = [
        'llama-server',
        '-hf', model_uri,
        '--host', '127.0.0.1',
        '--port', str(LLAMA_SERVER_PORT),
    ] + extra
    model_name_alphanumeric = re.sub(r'[^a-zA-Z0-9]', '_', model_uri)
    log_path = f'/tmp/llama.cpp.{model_name_alphanumeric}.log'
    with open(log_path, 'w') as log:
        with subprocess.Popen(cmd, stdout=log, stderr=log) as process:
            exit.wait()
            process.terminate()
            process.wait()


def main(
    model: str = typer.Option(
        DEFAULT_MODEL,
        '--model',
        help='HuggingFace model URI for llama-server.',
    ),
    agent: str = typer.Option(
        'opencode',
        '--agent',
        help='Agent to run (claude or opencode).',
    ),
    web: bool = typer.Option(
        False,
        '--web',
        help='Use web mode.',
    ),
    extra: list[str] = typer.Argument(None),
) -> None:
    ensure_attribution_header_disabled()
    exit_event = threading.Event()
    llama_server_download(model)
    llama_server_thread = threading.Thread(
        target=llama_server_worker,
        args=(model, exit_event),
        daemon=True,
    )
    llama_server_thread.start()

    if agent == 'opencode':
        ensure_opencode_config(model, web)
    else:
        os.environ['ANTHROPIC_AUTH_TOKEN'] = 'llama.cpp'
        os.environ['ANTHROPIC_BASE_URL'] = LLAMA_SERVER_URL

    if web and agent == 'opencode':
        cmd = [agent, 'web', '--port', '4096']
    else:
        cmd = [agent, '--model', model]
    if extra:
        cmd += extra
    subprocess.run(cmd, check=False)

    exit_event.set()
    llama_server_thread.join(timeout=1)


if __name__ == '__main__':
    typer.run(main)
