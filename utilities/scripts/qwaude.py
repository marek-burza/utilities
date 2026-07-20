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
    'prism-ml/Bonsai-27B-gguf:Q1_0': [
        '-ngl', '99',
        '-c', '262144',
        '-fa', 'on',
        '-np', '1',
        '--no-context-shift',
        '--cache-type-k', 'q4_0',  # Bonsai recommends 4-bit KV-cache quantization for on-device inference
        '--cache-type-v', 'q4_0',
        '--jinja',  # Correct chat-template / reasoning handling
        '--reasoning', 'on',
        '--reasoning-budget', '2048',  # Caps thinking, anti-loop guard
        '--temp', '0.7',  # Bonsai thinking-mode recommendation (Qwen3.6 uses 0.6)
        '--top-p', '0.95',
        '--top-k', '20',
        '--min-p', '0',
        '--presence-penalty', '1.1',  # Primary anti-looping lever
        '-b', '4096',  # Batch tuning (max number of tokens llama.cpp accepts into one processing call)
        '-ub', '2048',  # Ubatch tuning (how many tokens are actually computed together in a single GPU pass, and the one that grows your VRAM compute buffer)
        '--threads', str(cpu_count(logical=False)),
    ],
    'unsloth/gemma-4-31B-it-GGUF:IQ4_XS': [
        '-ngl', '99',
        '-c', '131072',
        '-fa', 'on',
        '-np', '1',
        '--no-context-shift',
        '--cache-type-k', 'q4_0',
        '--cache-type-v', 'q4_0',
        '--jinja',  # Correct chat-template handling (Gemma turn markers)
        '--temp', '1.0',
        '--top-p', '0.95',
        '--top-k', '64',
        '--min-p', '0',
        '-b', '4096',  # Batch tuning (max number of tokens llama.cpp accepts into one processing call)
        '-ub', '2048',  # Ubatch tuning (how many tokens are actually computed together in a single GPU pass, and the one that grows your VRAM compute buffer)
        '--threads', str(cpu_count(logical=False)),
    ],
    'google/gemma-4-31B-it-qat-q4_0-gguf': [
        '-ngl', '99',
        '-c', '262144',
        '-fa', 'on',
        '-np', '1',
        '--no-context-shift',
        '--cache-type-k', 'q4_0',
        '--cache-type-v', 'q4_0',
        '--jinja',  # Correct chat-template handling (Gemma turn markers)
        '--temp', '1.0',
        '--top-p', '0.95',
        '--top-k', '64',
        '--min-p', '0',
        '-b', '4096',  # Batch tuning (max number of tokens llama.cpp accepts into one processing call)
        '-ub', '2048',  # Ubatch tuning (how many tokens are actually computed together in a single GPU pass, and the one that grows your VRAM compute buffer)
        '--threads', str(cpu_count(logical=False)),
    ],
}
DEFAULT_MODEL = 'prism-ml/Bonsai-27B-gguf:Q1_0'


def llama_server_download(model_uri: str) -> None:
    with subprocess.Popen(['llama-cli', '-hf', model_uri, '-n', '0'], stdin=subprocess.PIPE, text=True) as process:
        process.stdin.write('/exit\n')
        process.stdin.close()
        process.wait()


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

    os.environ['ANTHROPIC_AUTH_TOKEN'] = 'llama.cpp'
    os.environ['ANTHROPIC_BASE_URL'] = LLAMA_SERVER_URL

    cmd = ['claude', '--model', model]
    if extra:
        cmd += extra
    subprocess.run(cmd, check=False)

    exit_event.set()
    llama_server_thread.join(timeout=1)


if __name__ == '__main__':
    typer.run(main)
