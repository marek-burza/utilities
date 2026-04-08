#!/usr/bin/env -S uv run --script
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "accelerate",
#     "librosa",
#     "mistral-common",
#     "numpy",
#     "pillow",
#     "soundfile",
#     "torch",
#     "torchvision",
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
import os
import queue
import tempfile
import threading
import subprocess
import sys
import warnings

import numpy as np
import soundfile as sf
import torch
import typer
from transformers import (
    CohereAsrForConditionalGeneration,
    CohereAsrProcessor,
    Gemma4ForConditionalGeneration,
    Gemma4Processor,
    VoxtralForConditionalGeneration,
    VoxtralProcessor,
    WhisperForConditionalGeneration,
    WhisperProcessor,
    pipeline,
)
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


class Model(str, enum.Enum):
    WHISPER = 'whisper'
    COHERE = 'cohere'
    VOXTRAL = 'voxtral'
    GEMMA = 'gemma'


MODEL_TO_HUGGINGFACE_ID = {
    Model.WHISPER: 'openai/whisper-large-v3',
    Model.COHERE: 'CohereLabs/cohere-transcribe-03-2026',  # https://cohere.com/blog/transcribe
    Model.VOXTRAL: 'mistralai/Voxtral-Mini-3B-2507',
    Model.GEMMA: 'google/gemma-4-E4B-it',
}


class WhisperPipeline:
    def __init__(self, model_id: str, device: str, dtype: torch.dtype) -> None:
        asr_model = WhisperForConditionalGeneration.from_pretrained(
            model_id, torch_dtype=dtype, low_cpu_mem_usage=True, use_safetensors=True
        ).to(device)
        processor = WhisperProcessor.from_pretrained(model_id)
        self._pipe = pipeline(
            'automatic-speech-recognition',
            model=asr_model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            dtype=dtype,
            device=device,
            batch_size=1,
        )
        self._pipe.model.generation_config.language = 'en'
        self._pipe.model.generation_config.task = 'transcribe'
        self._pipe.model.generation_config.no_repeat_ngram_size = 3
        self._pipe.model.generation_config.forced_decoder_ids = None

    def __call__(self, audio: np.ndarray) -> dict:
        return self._pipe(audio)


class CoherePipeline:
    def __init__(self, model_id: str, device: str, dtype: torch.dtype) -> None:
        asr_model = CohereAsrForConditionalGeneration.from_pretrained(
            model_id, torch_dtype=dtype, low_cpu_mem_usage=True, use_safetensors=True
        ).to(device)
        processor = CohereAsrProcessor.from_pretrained(model_id)
        self._pipe = pipeline(
            'automatic-speech-recognition',
            model=asr_model,
            tokenizer=processor.tokenizer,
            feature_extractor=processor.feature_extractor,
            dtype=dtype,
            device=device,
            batch_size=1,
        )

    def __call__(self, audio: np.ndarray) -> dict:
        return self._pipe(audio)


class VoxtralPipeline:
    def __init__(self, model_id: str, device: str, dtype: torch.dtype) -> None:
        self.device = device
        self.processor = VoxtralProcessor.from_pretrained(model_id)
        self.model = VoxtralForConditionalGeneration.from_pretrained(
            model_id, torch_dtype=dtype, low_cpu_mem_usage=True, use_safetensors=True
        ).to(device)

    def __call__(self, audio: np.ndarray) -> dict:
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
            tmp_path = f.name
        try:
            sf.write(tmp_path, audio, SAMPLE_RATE)
            messages = [{'role': 'user', 'content': [
                {'type': 'audio', 'url': tmp_path},
                {'type': 'text', 'text': 'Transcribe the audio.'},
            ]}]
            inputs = self.processor.apply_chat_template(
                messages, chat_template='', tokenize=True, return_dict=True,
                return_tensors='pt', add_generation_prompt=True,
            ).to(self.device)
        finally:
            os.unlink(tmp_path)
        prompt_len = inputs['input_ids'].shape[1]
        outputs = self.model.generate(**inputs, max_new_tokens=500)
        text = self.processor.decode(outputs[0][prompt_len:], skip_special_tokens=True)
        return {'text': text}


class GemmaPipeline:
    def __init__(self, model_id: str, device: str, dtype: torch.dtype) -> None:
        self.device = device
        self.processor = Gemma4Processor.from_pretrained(model_id)
        self.model = Gemma4ForConditionalGeneration.from_pretrained(
            model_id, torch_dtype=dtype, low_cpu_mem_usage=True,
        ).to(device)

    def __call__(self, audio: np.ndarray) -> str:
        with tempfile.NamedTemporaryFile(suffix='.wav') as f:
            tmp_path = f.name
            sf.write(tmp_path, audio, SAMPLE_RATE)
            messages = [{'role': 'user', 'content': [
                {'type': 'audio', 'url': tmp_path},
                {'type': 'text', 'text': 'Transcribe the audio.'},
            ]}]
            inputs = self.processor.apply_chat_template(
                messages, tokenize=True, return_dict=True,
                return_tensors='pt', add_generation_prompt=True,
            ).to(self.device)
            prompt_len = inputs['input_ids'].shape[1]
            outputs = self.model.generate(**inputs, max_new_tokens=500, do_sample=False)
            text = self.processor.decode(outputs[0][prompt_len:], skip_special_tokens=True)
            return {'text': text}


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
    model: Model = typer.Option(
        Model.WHISPER,
        '--model', '-m',
        help='Model used for transcription. Set HF_TOKEN if necessary.',
    ),
) -> None:
    sources = pulse_sources()
    if list_devices:
        print('\n'.join([f'{i}. {source.name}' for i, source in enumerate(sources)]))
        return

    print('Loading model...')
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_type = model
    model_id = MODEL_TO_HUGGINGFACE_ID[model_type]
    match model_type:
        case Model.WHISPER:
            pipe = WhisperPipeline(model_id, device, dtype)
        case Model.COHERE:
            pipe = CoherePipeline(model_id, device, dtype)
        case Model.VOXTRAL:
            pipe = VoxtralPipeline(model_id, device, dtype)
        case Model.GEMMA:
            pipe = GemmaPipeline(model_id, device, dtype)
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
