#!/usr/bin/env -S uv run --script
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "anthropic",
#     "accelerate",
#     "librosa",
#     "mistral-common",
#     "numpy",
#     "pillow",
#     "pytest",
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

import base64
import dataclasses
import enum
import logging
import os
import queue
import subprocess
import sys
import tempfile
import threading
import time
import warnings
from io import BytesIO

import anthropic
import numpy as np
import soundfile as sf
import torch
import typer
from PIL import ImageGrab
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

"""
Energy-envelope Voice Activity Detection (VAD).

Note: A frame is a small fixed-size slice of audio samples — the unit the VAD processes
one at a time rather than all at once.
At 16 kHz, 20 ms = 320 samples. Each call to vad.feed() receives exactly that array.
We are using 20 ms as a default because it is a standard in speech processing because
it matches the typical time scale of a phoneme - short enough that speech/silence transitions
are detected quickly, but long enough that the RMS energy measurement is stable
and not fooled by individual waveform peaks.
At 10 ms you get noisier energy estimates; at 40 ms you start missing fast transitions.
"""
class VadAccumulator:
    def __init__(
        self,
        frame_ms: int = 20,
        energy_threshold: float = 0.01,
        min_silence_ms: int = 600,
        min_speech_ms: int = 300,
        max_speech_ms: int = 15000,
    ) -> None:
        self.frame_samples = SAMPLE_RATE * frame_ms // 1000
        self._min_silence_frames = min_silence_ms // frame_ms
        self._min_speech_frames = min_speech_ms // frame_ms
        self._max_speech_samples = int(max_speech_ms / 1000 * SAMPLE_RATE)
        self._energy_threshold = energy_threshold
        self._buffer: list[np.ndarray] = []
        self._speech_frames = 0
        self._silence_frames = 0
        self._in_speech = False

    def feed(self, frame: np.ndarray) -> np.ndarray | None:
        is_speech = np.sqrt(np.mean(frame ** 2)) >= self._energy_threshold
        if is_speech:
            self._buffer.append(frame)
            self._speech_frames += 1
            self._silence_frames = 0
            self._in_speech = True
            if sum(len(frame) for frame in self._buffer) >= self._max_speech_samples:
                return self.flush()
        elif self._in_speech:
            self._buffer.append(frame)
            self._silence_frames += 1
            if self._silence_frames >= self._min_silence_frames:
                return self.flush()
        return None

    def flush(self) -> np.ndarray | None:
        segment: np.ndarray | None = None
        if self._speech_frames >= self._min_speech_frames:
            segment = np.concatenate(self._buffer)
        # Reset buffer
        self._buffer = []
        self._speech_frames = 0
        self._silence_frames = 0
        self._in_speech = False
        return segment


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
        result = pipe(chunk.data)
        text = result['text'].strip()
        if text:
            prefix = f'[{chunk.origin}] ' if multi_source else ''
            sys.stdout.write(f'{prefix}{text}\n')
            sys.stdout.flush()


def capture_worker(
    device: str,
    origin: str,
    audio: queue.Queue[Chunk | None],
    exit: threading.Event,
    vad: VadAccumulator,
) -> None:
    cmd = [
        'ffmpeg', '-loglevel', 'quiet',
        '-f', 'pulse', '-i', device,
        '-f', 's16le', '-ar', str(SAMPLE_RATE), '-ac', '1',
        'pipe:1',
    ]
    frame_bytes = vad.frame_samples * BYTES_PER_SAMPLE
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL) as process:
        try:
            while not exit.is_set():
                raw = process.stdout.read(frame_bytes)
                if not raw:
                    break
                frame = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
                segment = vad.feed(frame)
                if segment is not None:
                    audio.put(Chunk(origin, segment))
            remainder = vad.flush()
            if remainder is not None:
                audio.put(Chunk(origin, remainder))
        finally:
            process.terminate()
            process.wait()


PROMPT_OCR = """
Describe what is on this screen. Extract any visible text,"
summarize diagrams or plots, capture assignments/tasks/questions verbatim,
and take a separate note of any partial solutions."
"""

def capture_screen_contents():
    agent = anthropic.Anthropic(
        base_url='http://localhost:11434',  # host.docker.internal
        api_key='ollama',
    )
    while True:
        try:
            screenshot = ImageGrab.grab()
            buffer = BytesIO()
            screenshot.save(buffer, format='PNG')
            png_base64 = base64.b64encode(buffer.getvalue()).decode()
            message = agent.messages.create(
                # model='mistral-small3.1:24b',
                # model='gemma4:26b',
                model='gemma3:12b',
                max_tokens=4096,
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'image',
                                'source': {
                                    'type': 'base64',
                                    'media_type': 'image/png',
                                    'data': png_base64,
                                },
                            },
                            {'type': 'text', 'text': PROMPT_OCR},
                        ],
                    }
                ],
            )
            text = next(
                block.text for block in message.content if block.type == 'text'
            )
            print(f"\n[{time.strftime('%H:%M:%S')}] {text}")
        except Exception as e:
            print(f"\n[{time.strftime('%H:%M:%S')}] Error: {e}")
        # time.sleep(2)


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
    min_silence_ms: int = typer.Option(
        600,
        '--min-silence-ms',
        help='Milliseconds of silence required to end a speech segment.',
    ),
    max_speech_ms: int = typer.Option(
        15000,
        '--max-speech-ms',
        help='Maximum milliseconds of speech before forcing a speech segment boundary.',
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
        vad = VadAccumulator(min_silence_ms=min_silence_ms, max_speech_ms=max_speech_ms)
        capture_thread = threading.Thread(
            target=capture_worker,
            args=(device, 'local', audio, exit, vad),
            daemon=True,
        )
        capture_threads.append(capture_thread)
    if source in (Source.SPEAKER, Source.BOTH):
        device = default_speaker_device(sources, speaker_device)
        vad = VadAccumulator(min_silence_ms=min_silence_ms, max_speech_ms=max_speech_ms)
        capture_thread = threading.Thread(
            target=capture_worker,
            args=(device, 'remote', audio, exit, vad),
            daemon=True,
        )
        capture_threads.append(capture_thread)
    # if source in (Source.SCREEN, Source.ALL):
    #     capture_thread = threading.Thread(
    #         target=capture_screen_contents,
    #         daemon=True,
    #     )
    #     capture_threads.append(capture_thread)
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


# Tests — run with: uv run --with pytest --with numpy --with soundfile --with torch --with torchvision --with transformers --with typer --with accelerate --with librosa --with pillow --with mistral-common python -m pytest utilities/scripts/live.py -v
class TestVadAccumulator:
    _FRAME_SAMPLES = SAMPLE_RATE * 20 // 1000  # 320 samples per 20ms frame

    @staticmethod
    def _make_speech_frame(energy: float = 0.05) -> np.ndarray:
        t = np.linspace(0, 20 / 1000, TestVadAccumulator._FRAME_SAMPLES, endpoint=False)
        return (energy * np.sin(2 * np.pi * 440 * t)).astype(np.float32)

    @staticmethod
    def _make_silent_frame() -> np.ndarray:
        return np.zeros(TestVadAccumulator._FRAME_SAMPLES, dtype=np.float32)

    def test_silence_only_emits_nothing(self):
        vad = VadAccumulator()
        for _ in range(200):
            assert vad.feed(TestVadAccumulator._make_silent_frame()) is None
        assert vad.flush() is None

    def test_speech_then_silence_emits_segment(self):
        vad = VadAccumulator(min_silence_ms=600, min_speech_ms=300)
        for _ in range(25):  # 500ms speech
            result = vad.feed(TestVadAccumulator._make_speech_frame())
            assert result is None
        segment = None
        for _ in range(35):  # 700ms silence
            result = vad.feed(TestVadAccumulator._make_silent_frame())
            if result is not None:
                segment = result
                break
        assert segment is not None
        assert len(segment) >= 25 * TestVadAccumulator._FRAME_SAMPLES

    def test_short_speech_below_min_is_discarded(self):
        vad = VadAccumulator(min_silence_ms=200, min_speech_ms=500)
        for _ in range(5):  # 100ms speech
            vad.feed(TestVadAccumulator._make_speech_frame())
        for _ in range(50):
            result = vad.feed(TestVadAccumulator._make_silent_frame())
            assert result is None

    def test_brief_silence_does_not_split(self):
        vad = VadAccumulator(min_silence_ms=600, min_speech_ms=300)
        for _ in range(25):
            vad.feed(TestVadAccumulator._make_speech_frame())
        for _ in range(10):  # 200ms silence
            assert vad.feed(TestVadAccumulator._make_silent_frame()) is None
        for _ in range(25):
            assert vad.feed(TestVadAccumulator._make_speech_frame()) is None
        segment = None
        for _ in range(35):
            result = vad.feed(TestVadAccumulator._make_silent_frame())
            if result is not None:
                segment = result
                break
        assert segment is not None
        assert len(segment) >= 50 * TestVadAccumulator._FRAME_SAMPLES

    def test_max_speech_cap_forces_emit(self):
        vad = VadAccumulator(max_speech_ms=1000)
        segment = None
        for _ in range(75):  # 1.5s continuous speech
            result = vad.feed(TestVadAccumulator._make_speech_frame())
            if result is not None:
                segment = result
                break
        assert segment is not None
        expected = int(1.0 * SAMPLE_RATE)
        assert abs(len(segment) - expected) < TestVadAccumulator._FRAME_SAMPLES * 2

    def test_flush_returns_accumulated_speech(self):
        vad = VadAccumulator(min_speech_ms=300)
        for _ in range(25):
            vad.feed(TestVadAccumulator._make_speech_frame())
        segment = vad.flush()
        assert segment is not None
        assert len(segment) == 25 * TestVadAccumulator._FRAME_SAMPLES

    def test_flush_on_empty_returns_none(self):
        vad = VadAccumulator()
        assert vad.flush() is None
