#!/usr/bin/env -S uv run --script --quiet
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
# ]
# ///

import os
import re
import subprocess
import threading
import time
import urllib.request

import typer


DEFAULT_MODEL = 'unsloth/Qwen3.6-27B-GGUF:UD-Q4_K_XL'
LLAMA_SERVER_PORT = 8080
LLAMA_SERVER_URL = f'http://127.0.0.1:{LLAMA_SERVER_PORT}'
LLAMA_SERVER_EXTRA_PARAMS: dict[str, list[str]] = {
    DEFAULT_MODEL: [
        '-ngl', '99',
        '-c', '262144',
        '-fa', 'on',
        '--no-context-shift',
        '--cache-type-k', 'q4_0',
        '--cache-type-v', 'q4_0',
        '--reasoning', 'on',
        '--temp', '0.6',
        '--top-p', '0.95',
        '--top-k', '20',
        '--min-p', '0',
        '--presence-penalty', '0',
    ],
    'unsloth/gemma-4-31B-it-GGUF:UD-Q5_K_XL': [
        '-ngl', '99',
        '-c', '262144',
        '-fa', 'on',
        '--no-context-shift',
        '--cache-type-k', 'q4_0',
        '--cache-type-v', 'q4_0',
        '--temp', '1.0',
        '--top-p', '0.95',
        '--top-k', '64',
        '--min-p', '0',
    ],
    'unsloth/MiniMax-M2.7-GGUF:UD-IQ4_XS': [
        '-ngl', '20',
        '-c', '65536',
        '--cache-type-k', 'q4_0',
        '--cache-type-v', 'q4_0',
        '--temp', '1.0',
        '--top-p', '0.95',
        '--top-k', '40',
    ],
}


def llama_server_download(model_uri: str) -> None:
    with subprocess.Popen(['llama-cli', '-hf', model_uri, '-n', '0'], stdin=subprocess.PIPE, text=True) as process:
        process.stdin.write('/exit\n')
        process.stdin.close()
        process.wait()


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


def llama_server_wait(timeout: float = 120.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f'{LLAMA_SERVER_URL}/health', timeout=1)
            return
        except Exception:
            time.sleep(1)
    raise RuntimeError(f'llama-server did not become ready within {timeout}s')


def main(
    model: str = typer.Option(
        DEFAULT_MODEL,
        '--model',
        help='HuggingFace model URI for llama-server.',
    ),
) -> None:
    exit_event = threading.Event()
    llama_server_download(model)
    llama_server_thread = threading.Thread(
        target=llama_server_worker,
        args=(model, exit_event),
        daemon=True,
    )
    llama_server_thread.start()
    llama_server_wait()

    os.environ['ANTHROPIC_AUTH_TOKEN'] = 'llama.cpp'
    os.environ['ANTHROPIC_BASE_URL'] = LLAMA_SERVER_URL
    os.system(f'claude --model {model}')

    exit_event.set()
    llama_server_thread.join(timeout=1)


if __name__ == '__main__':
    typer.run(main)
