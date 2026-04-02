#!/usr/bin/env -S uv run --script
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "accelerate",
#     "numpy",
#     "torch",
#     "transformers",
#     "typer",
# ]
# ///
# Transcribes live audio from microphone and/or speaker playback (loopback).
# Captures audio via ffmpeg using PulseAudio sources.
# Run with --list-devices to find available source names.

import dataclasses
import enum
import logging
import queue
import threading
import subprocess
import sys
import warnings

import numpy as np
import torch
import typer
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from transformers.utils import logging as transformers_logging


warnings.filterwarnings('ignore', message='A custom logits processor of type')
warnings.filterwarnings('ignore', message='You seem to be using the pipelines sequentially on GPU')
warnings.filterwarnings('ignore', message='You are sending unauthenticated requests')
transformers_logging.set_verbosity_error()
logging.getLogger('huggingface_hub').setLevel(logging.ERROR)


SAMPLE_RATE = 16000
BYTES_PER_SAMPLE = 2  # int16 / s16le


class Source(str, enum.Enum):
    MICROPHONE = 'microphone'
    SPEAKER = 'speaker'
    BOTH = 'both'


@dataclasses.dataclass
class Device:
    default: bool
    device: str
    name: str


@dataclasses.dataclass
class Chunk:
    origin: str
    data: np.ndarray


def pulse_sources() -> list[Device]:
    result = subprocess.run(
        ['ffmpeg', '-sources', 'pulse'],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.splitlines()
    sources = []
    listing = False
    for line in lines:
        if line.startswith('Auto-detected'):
            listing = True
            continue
        if listing:
            default = line.startswith('*')
            line = line[2:]
            device = line[:line.index(' ')]
            name = line[line.index('[') + 1 : line.index(']')]
            sources.append(Device(default, device, name))
    return sources


def default_microphone_device(sources: list[Device], override: int | None) -> str:
    try:
        if override:
            return sources[override].device
        return [source.device for source in sources if source.default][0]
    except:
        raise RuntimeError(
            'No microphone source found. Specify one with --microphone-device.\n'
            'Run with --list-devices to see available sources.'
        )


def default_speaker_device(sources: list[Device], override: int | None) -> str:
    try:
        if override:
            return sources[override].device
        return [source.device for source in sources if source.device.endswith('.monitor')][0]
    except:
        raise RuntimeError(
            'No monitor source found. Specify one with --speaker-device.\n'
            'Run with --list-devices to see available sources.'
        )


def transcribe_worker(
    pipe: pipeline,
    multi_source: bool,
    audio: queue.Queue[Chunk | None],
    exit: threading.Event,
) -> None:
    while not exit.is_set():
        chunk = audio.get()
        if chunk is None:
            break
        if np.sqrt(np.mean(chunk.data ** 2)) >= 0.01:
            result = pipe(chunk.data)
            text = result['text'].strip()
            if text:
                prefix = f'[{chunk.origin}] ' if multi_source else ''
                sys.stdout.write(f'{prefix}{text} ')
                sys.stdout.flush()


def capture_worker(
    device: str,
    chunk_seconds: int,
    origin: str,
    audio: queue.Queue[Chunk | None],
    exit: threading.Event,
) -> None:
    cmd = [
        'ffmpeg', '-loglevel', 'quiet',
        '-f', 'pulse', '-i', device,
        '-f', 's16le', '-ar', str(SAMPLE_RATE), '-ac', '1',
        'pipe:1',
    ]
    chunk_bytes = SAMPLE_RATE * chunk_seconds * BYTES_PER_SAMPLE
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as process:
        try:
            while not exit.is_set():
                raw = process.stdout.read(chunk_bytes)
                if not raw:
                    break
                if len(raw) < chunk_bytes:
                    raw += b'\x00' * (chunk_bytes - len(raw))
                data = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
                audio.put(Chunk(origin.value, data))
        finally:
            process.terminate()
            process.wait()


def main(
    list_devices: bool = typer.Option(
        False,
        '--list-devices',
        help='List available PulseAudio sources and exit.',
    ),
    source: Source = typer.Option(
        Source.BOTH,
        '--source', '-s',
        help='Audio source to transcribe: mic, speaker (loopback), or both.',
    ),
    microphone_device: int | None = typer.Option(
        None,
        '--microphone-device',
        help='PulseAudio source index for microphone. Auto-detected if not provided.',
    ),
    speaker_device: int | None = typer.Option(
        None,
        '--speaker-device',
        help='PulseAudio source index for speaker (loopback). Auto-detected if not provided.',
    ),
    chunk_seconds: int = typer.Option(
        4,
        '--chunk-seconds',
        help='Seconds of audio to accumulate before each transcription pass.',
    ),
) -> None:
    sources = pulse_sources()
    if list_devices:
        print('\n'.join([f'{i}. {source.name}' for i, source in enumerate(sources)]))
        return

    print('Loading model...')
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = 'openai/whisper-large-v3'
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, dtype=dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    pipe = pipeline(
        'automatic-speech-recognition',
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        dtype=dtype,
        device=device,
        batch_size=1,
    )
    pipe.model.generation_config.language = 'en'
    pipe.model.generation_config.task = 'transcribe'
    pipe.model.generation_config.no_repeat_ngram_size = 3
    pipe.model.generation_config.forced_decoder_ids = None
    print('Model loaded. Listening... (Ctrl+C to exit)')

    audio: queue.Queue[Chunk | None] = queue.Queue()
    multi_source = source == Source.BOTH
    exit = threading.Event()

    transcriber = threading.Thread(
        target=transcribe_worker,
        args=(pipe, multi_source, audio, exit),
        daemon=True,
    )
    transcriber.start()

    capture_threads: list[threading.Thread] = []
    if source in (Source.MICROPHONE, Source.BOTH):
        device = default_microphone_device(sources, microphone_device)
        capture_thread = threading.Thread(
            target=capture_worker,
            args=(device, chunk_seconds, Source.MICROPHONE, audio, exit),
            daemon=True,
        )
        capture_threads.append(capture_thread)
    if source in (Source.SPEAKER, Source.BOTH):
        device = default_speaker_device(sources, speaker_device)
        capture_thread = threading.Thread(
            target=capture_worker,
            args=(device, chunk_seconds, Source.SPEAKER, audio, exit),
            daemon=True,
        )
        capture_threads.append(capture_thread)
    for capture_thread in capture_threads:
        capture_thread.start()

    try:
        for capture_thread in capture_threads:
            capture_thread.join()
    except KeyboardInterrupt:
        print('\nStopping...')
        exit.set()
        for capture_thread in capture_threads:
            capture_thread.join(timeout=1)
    finally:
        audio.put(None)
        transcriber.join(timeout=1)


if __name__ == '__main__':
    typer.run(main)
