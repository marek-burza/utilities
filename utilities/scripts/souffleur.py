#!/usr/bin/env -S uv run --script
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "langchain-openai",
#     "accelerate",
#     "huggingface-hub",
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
import re
import subprocess
import tempfile
import threading
import time
import warnings
from io import BytesIO

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import numpy as np
import soundfile as sf
import torch
import typer
from PIL import ImageGrab
from transformers import (
    AutoProcessor,
    CohereAsrForConditionalGeneration,
    CohereAsrProcessor,
    Gemma4ForConditionalGeneration,
    Gemma4Processor,
    Qwen2_5_VLForConditionalGeneration,
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
    AUDIO = 'audio'
    SCREEN = 'screen'
    ALL = 'all'


class Model(str, enum.Enum):
    WHISPER = 'whisper'
    COHERE = 'cohere'
    VOXTRAL = 'voxtral'
    GEMMA = 'gemma'


class OcrMode(str, enum.Enum):
    GENERIC = 'generic'
    NANONETS = 'nanonets'


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


LLAMA_SERVER_BASE_PORT = 8080

# Extra CLI args passed to llama-server per model URI.
# -fa (flash attention) is required when using KV cache quantization and recommended for all GPU use.
# --cache-type-k/v q8_0 halves KV VRAM vs fp16 default with negligible quality loss; requires -fa.
# Qwen3/Gemma4 have thinking/CoT mode ON by default — --reasoning off disables it (no benefit here, wastes tokens).
# --jinja is now implicit in recent llama.cpp builds; --reasoning off supersedes --chat-template-kwargs enable_thinking.
# --no-context-shift prevents silent token rotation on Qwen3; generation halts at limit instead.
# phi-4 has a hard 16K context ceiling — do not set -c above 16384.
LLAMA_SERVER_EXTRA_PARAMS: dict[str, list[str]] = {
    # --- OCR models (vision, screen capture → extract text/diagrams/questions) ---
    'ggml-org/Qwen2.5-VL-7B-Instruct-GGUF': [
        '-c', '8192', '-fa', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--temp', '0.1',
    ],
    'ggml-org/Mistral-Small-3.1-24B-Instruct-2503-GGUF': [
        '-c', '16384', '-fa', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--temp', '0.15',
    ],
    # gemma-3-12b also used for solving; 12K covers both roles
    'ggml-org/gemma-3-12b-it-GGUF': [
        '-c', '12288', '-fa', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
    ],
    # gemma-4 also used for solving; 16K covers both roles; thinking disabled
    'unsloth/gemma-4-E4B-it-GGUF': [
        '-c', '16384', '-fa', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--reasoning', 'off',
    ],
    # --- Distillation models (long rolling transcript → identify most recent question) ---
    # 32K for transcript growth; thinking disabled; no-context-shift for pipeline safety
    'Qwen/Qwen3-8B-GGUF': [
        '-c', '32768', '-fa', 'on', '--no-context-shift',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--reasoning', 'off',
    ],
    # Qwen3-8B fine-tune (Q1_0, ~1.15 GB); requires PrismML fork: github.com/PrismML-Eng/llama.cpp
    # --cache-reuse 256 lets repeated transcript prefix tokens hit the prompt cache across calls
    'prism-ml/Bonsai-8B-gguf': [
        '-c', '32768', '-fa', 'on', '--no-context-shift',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--cache-reuse', '256',
        '--reasoning', 'off',
    ],
    # QAT-quantized — q8_0 KV is fine; text-only (no mmproj shipped)
    'google/gemma-3-4b-it-qat-q4_0-gguf': [
        '-c', '32768', '-fa', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
    ],
    # phi-4 also used for solving; 16K is the hard ceiling for both roles
    'microsoft/phi-4-gguf': [
        '-c', '16384', '-fa', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
    ],
    # --- Solving models (short assignment → concise bullet-point answer) ---
    # 8K is ample for solve; thinking disabled for speed; no-context-shift for pipeline safety
    'Qwen/Qwen3-14B-GGUF': [
        '-c', '8192', '-fa', 'on', '--no-context-shift',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--reasoning', 'off',
    ],
    'bartowski/Mistral-Small-Instruct-2409-GGUF': [
        '-c', '8192', '-fa', 'on',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--temp', '0.3',
    ],
    # Qwen3.6-35B-A3B: MoE+SSM hybrid (qwen35moe arch), 3B active of 35B total.
    # Requires llama.cpp b4000+ for qwen35moe support. Avoid CUDA 13.2 (produces garbled output; use 12.x).
    'bartowski/Qwen_Qwen3.6-35B-A3B-GGUF': [
        '-c', '32768', '-fa', 'on', '--no-context-shift',
        '--cache-type-k', 'q8_0', '--cache-type-v', 'q8_0',
        '--reasoning', 'off',
    ],
}


def llama_server_download(model_uri: str) -> None:
    with subprocess.Popen(['llama-cli', '-hf', model_uri, '-n', '0'], stdin=subprocess.PIPE, text=True) as process:
        process.stdin.write('/exit\n')
        process.stdin.close()
        process.wait()


def llama_server_worker(model_uri: str, port: int, exit: threading.Event) -> None:
    extra = LLAMA_SERVER_EXTRA_PARAMS.get(model_uri, [])
    cmd = [
        'llama-server', '-hf', model_uri, '-ngl', '99',
        '--host', '127.0.0.1', '--port', str(port),
    ] + extra

    model_name_alphanumeric = re.sub(r'[^a-zA-Z0-9]', '_', model_uri)
    log_path = f'/tmp/llama.cpp.{model_name_alphanumeric}.log'
    with open(log_path, 'w') as log:
        with subprocess.Popen(cmd, stdout=log, stderr=log) as process:
            exit.wait()
            process.terminate()
            process.wait()


PROMPT_OCR_NANONETS = 'Extract all text, preserving code structure and formatting.'


class NanonetsPipeline:
    MODEL_ID = 'nanonets/Nanonets-OCR-s'

    def __init__(self, device: str, dtype: torch.dtype) -> None:
        self.device = device
        self.processor = AutoProcessor.from_pretrained(self.MODEL_ID)
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            self.MODEL_ID, torch_dtype=dtype, low_cpu_mem_usage=True, use_safetensors=True
        ).to(device)

    def __call__(self, image) -> str:
        messages = [{'role': 'user', 'content': [
            {'type': 'image'},
            {'type': 'text', 'text': PROMPT_OCR_NANONETS},
        ]}]
        text = self.processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = self.processor(text=[text], images=[image], return_tensors='pt').to(self.device)
        prompt_len = inputs['input_ids'].shape[1]
        outputs = self.model.generate(**inputs, max_new_tokens=2048)
        return self.processor.decode(outputs[0][prompt_len:], skip_special_tokens=True)


@dataclasses.dataclass
class Device:
    default: bool
    device: str
    name: str


@dataclasses.dataclass
class Chunk:
    origin: str
    data: np.ndarray


@dataclasses.dataclass
class SessionState:
    transcript: str = ''
    screen_contents: str = ''
    assignment: str = ''
    solution: str = ''
    lock: threading.Lock = dataclasses.field(
        default_factory=threading.Lock, init=False, repr=False, compare=False
    )

    def add_transcript(self, text: str) -> None:
        with self.lock:
            self.transcript += text + '\n'
            with open('transcript.txt', 'w') as handle:
                handle.write(self.transcript)

    def update_screen(self, contents: str) -> None:
        with self.lock:
            self.screen_contents = contents

    def update_assignment(self, text: str) -> None:
        with self.lock:
            self.assignment = text

    def update_solution(self, text: str) -> None:
        with self.lock:
            self.solution = text

    def snapshot(self) -> tuple[str, str, str]:
        with self.lock:
            return self.transcript, self.screen_contents, self.assignment

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

For noisier environments (music, HVAC, keyboard) the RMS threshold false-triggers and
sends non-speech segments to the ASR model. A drop-in replacement using `silero-vad`
(~1.8 MB JIT model, sub-ms inference per 32 ms frame) keeps the same feed/flush
contract (would need to fix the window to 512 samples (Silero's 16 kHz requirement) and replace
the RMS check with model inference).
"""
class VadAccumulator:
    def __init__(
        self,
        frame_ms: int = 20,
        energy_threshold: float = 0.01,
        min_silence_ms: int = 800,
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


def pulse_devices(flag: str) -> list[Device]:
    result = subprocess.run(
        ['ffmpeg', flag, 'pulse'],
        capture_output=True,
        text=True,
    )
    devices = []
    listing = False
    for line in result.stdout.splitlines():
        if line.startswith('Auto-detected'):
            listing = True
            continue
        if listing:
            default = line.startswith('*')
            line = line[2:]
            device = line[:line.index(' ')]
            name = line[line.index('[') + 1 : line.index(']')]
            devices.append(Device(default, device, name))
    return devices


def pulse_sources() -> list[Device]:
    return pulse_devices('-sources')


def pulse_sinks() -> list[Device]:
    return pulse_devices('-sinks')


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
        default = [sink for sink in pulse_sinks() if sink.default][0].device + '.monitor'
        return [s.device for s in sources if s.device == default][0]
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
    state: SessionState,
) -> None:
    while not exit.is_set():
        chunk = audio.get()
        if chunk is None:
            break
        result = pipe(chunk.data)
        text = result['text'].strip()
        if text:
            prefix = f'[{chunk.origin}] ' if multi_source else ''
            state.add_transcript(f'{prefix}{text}')


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

def capture_screen_contents(
    state: SessionState,
    exit: threading.Event,
    client: ChatOpenAI | None,
    ocr_mode: OcrMode,
    interval: float = 0.0,
) -> None:
    nanonets_pipe: NanonetsPipeline | None = None
    if ocr_mode == OcrMode.NANONETS:
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        dtype = torch.float16 if torch.cuda.is_available() else torch.float32
        print('Loading Nanonets OCR model...')
        nanonets_pipe = NanonetsPipeline(device, dtype)
        print('Nanonets OCR model loaded.')
    while not exit.is_set():
        try:
            screenshot = ImageGrab.grab()
            if nanonets_pipe is not None:
                text = nanonets_pipe(screenshot)
            else:
                buffer = BytesIO()
                screenshot.save(buffer, format='PNG')
                png_base64 = base64.b64encode(buffer.getvalue()).decode()
                response = client.invoke([HumanMessage(content=[
                    {'type': 'image_url', 'image_url': {'url': f'data:image/png;base64,{png_base64}'}},
                    {'type': 'text', 'text': PROMPT_OCR},
                ])])
                text = response.content
            state.update_screen(text)
        except Exception as e:
            print(f'Error: {e}')
        time.sleep(interval)


PROMPT_SOLUTION = """
Solve the following assignment concisely.

<assignment>
{assignment}
</assignment>

Structure your response as:

TL;DR: <one or two sentences summarising the answer>

<detailed answer using bullet points — correct and complete, but no padding or repetition;
prefer bullet points over a block of text>
"""


PROMPT_ASSIGNMENT = """
You are monitoring a live transcript and screen capture for a student.
Your job is to identify the most recent question or task — the "assignment".

Below are the latest transcript and screen contents. Pay closest attention to
the END of the transcript — that is where the most recent question appears.

<transcript>
{transcript}
</transcript>

<screen_contents>
{screen_contents}
</screen_contents>

For reference, here is the previous assignment (may be empty):

<previous_assignment>
{assignment}
</previous_assignment>

Step 1 — Classify. Decide which case applies:
  A) A NEW question or task appears in the transcript or screen that is different
     from the previous assignment. This includes follow-up questions like
     "what do you mean by X?", "can you explain Y?", "why?" — these are NEW
     questions even if topically related.
  B) No new question, but there is new information (constraint, hint, correction)
     that refines the SAME task in the previous assignment.
  C) Nothing meaningful has changed.

Step 2 — Respond:
  Case A: Write a NEW assignment from scratch based ONLY on the new question.
          Do NOT include, merge, or reference any details from the previous
          assignment. Pretend the previous assignment does not exist.
  Case B: Write an updated version of the previous assignment incorporating
          the new details.
  Case C: Respond with exactly: NO_CHANGE

Your response must contain ONLY the assignment text (cases A/B) or NO_CHANGE
(case C). No preamble, no labels, no XML tags, no "Case A:" prefix.
"""


def strip_xml_tags(text: str) -> str:
    return re.sub(r'</?[a-zA-Z_][a-zA-Z0-9_]*>', '', text).strip()


def distiller_worker(
    state: SessionState,
    exit: threading.Event,
    client: ChatOpenAI,
    interval: float = 0.5,
) -> None:
    previous_transcript = ''
    previous_screen_contents = ''
    while not exit.is_set():
        transcript, screen_contents, assignment = state.snapshot()
        if transcript == previous_transcript and screen_contents == previous_screen_contents:
            time.sleep(interval)
            continue
        previous_transcript = transcript
        previous_screen_contents = screen_contents
        try:
            response = client.invoke([HumanMessage(content=PROMPT_ASSIGNMENT.format(
                assignment=assignment or '(none yet)',
                transcript=transcript or '(empty)',
                screen_contents=screen_contents or '(empty)',
            ))])
            text = response.content.strip()
            if text != 'NO_CHANGE':
                state.update_assignment(strip_xml_tags(text))
        except Exception as e:
            print(f'Distiller error: {e}')


def solver_worker(
    state: SessionState,
    exit: threading.Event,
    client: ChatOpenAI,
    interval: float = 0.5,
) -> None:
    previous_assignment = ''
    while not exit.is_set():
        _, _, assignment = state.snapshot()
        if assignment == previous_assignment or not assignment:
            time.sleep(interval)
            continue
        previous_assignment = assignment
        try:
            response = client.invoke([HumanMessage(content=PROMPT_SOLUTION.format(assignment=assignment))])
            text = response.content.strip()
            state.update_solution(text)
            print('\n===\n')
            print(state.assignment)
            print('\n---\n')
            print(state.solution)
            print('\n---\n')
        except Exception as e:
            print(f'Solver error: {e}')



def main(
    list_devices: bool = typer.Option(
        False,
        '--list-devices',
        help='List available PulseAudio sources and exit.',
    ),
    source: Source = typer.Option(
        Source.ALL,
        '--source',
        help='Audio source to transcribe: mic, speaker (loopback), screen or all.',
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
    transcribe_model: Model = typer.Option(
        Model.WHISPER,
        '--transcribe-model',
        help='Model used for transcription. Set HF_TOKEN if necessary.',
    ),
    ocr_mode: OcrMode = typer.Option(
        OcrMode.GENERIC,
        '--ocr-mode',
        help='Screen OCR mode: generic (VLM via LangChain/OpenAI-compatible endpoint) or nanonets (local Nanonets-OCR-s, best for code/text screens).',
    ),
    ocr_model: str = typer.Option(
        'ggml-org/Qwen2.5-VL-7B-Instruct-GGUF',
        '--ocr-model',
        help='HuggingFace model URI for llama-server used for screen OCR when --ocr-mode=generic (default is ggml-org/Qwen2.5-VL-7B-Instruct-GGUF, other good ones are unsloth/gemma-4-E4B-it-GGUF, ggml-org/Mistral-Small-3.1-24B-Instruct-2503-GGUF, ggml-org/gemma-3-12b-it-GGUF).',
    ),
    distill_model: str = typer.Option(
        'Qwen/Qwen3-8B-GGUF',
        '--distill-model',
        help='HuggingFace model URI for llama-server used for assignment distillation (default is Qwen/Qwen3-8B-GGUF, other good ones are google/gemma-3-4b-it-qat-q4_0-gguf, microsoft/phi-4-gguf).',
    ),
    solve_model: str = typer.Option(
        'Qwen/Qwen3-14B-GGUF',
        '--solve-model',
        help='HuggingFace model URI for llama-server used for solving assignments (default is Qwen/Qwen3-14B-GGUF, heavier one is unsloth/gemma-4-E4B-it-GGUF, similarly light are microsoft/phi-4-gguf, ggml-org/gemma-3-12b-it-GGUF, bartowski/Mistral-Small-Instruct-2409-GGUF).',
    ),
) -> None:
    sources = pulse_sources()
    if list_devices:
        print('\n'.join([f'{i}. {source.name}' for i, source in enumerate(sources)]))
        return

    print('Loading model...')
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_type = transcribe_model
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
    multi_source = source == Source.ALL or source == Source.AUDIO
    exit = threading.Event()
    state = SessionState()

    unique_models = list(dict.fromkeys([ocr_model, distill_model, solve_model]))
    model_to_port = {uri: LLAMA_SERVER_BASE_PORT + i for i, uri in enumerate(unique_models)}

    def make_client(uri: str) -> ChatOpenAI:
        port = model_to_port[uri]
        return ChatOpenAI(base_url=f'http://127.0.0.1:{port}/v1', api_key='llama.cpp', model=uri)

    distill_client = make_client(distill_model)
    solve_client = make_client(solve_model)
    ocr_client = make_client(ocr_model)

    threads: list[threading.Thread] = []
    for uri, port in model_to_port.items():
        llama_server_download(uri)
        threads.append(threading.Thread(
            target=llama_server_worker,
            args=(uri, port, exit),
            daemon=True,
        ))
    transcriber_thread = threading.Thread(
        target=transcribe_worker,
        args=(pipe, multi_source, audio, exit, state),
        daemon=True,
    )
    threads.append(transcriber_thread)
    if source in [Source.MICROPHONE, Source.AUDIO, Source.ALL]:
        device = default_microphone_device(sources, microphone_device)
        vad = VadAccumulator(min_silence_ms=min_silence_ms, max_speech_ms=max_speech_ms)
        capture_thread = threading.Thread(
            target=capture_worker,
            args=(device, 'local', audio, exit, vad),
            daemon=True,
        )
        threads.append(capture_thread)
    if source in [Source.SPEAKER, Source.AUDIO, Source.ALL]:
        device = default_speaker_device(sources, speaker_device)
        vad = VadAccumulator(min_silence_ms=min_silence_ms, max_speech_ms=max_speech_ms)
        capture_thread = threading.Thread(
            target=capture_worker,
            args=(device, 'remote', audio, exit, vad),
            daemon=True,
        )
        threads.append(capture_thread)
    if source in (Source.SCREEN, Source.ALL):
        capture_thread = threading.Thread(
            target=capture_screen_contents,
            args=(state, exit, ocr_client, ocr_mode),
            daemon=True,
        )
        threads.append(capture_thread)
    distiller_thread = threading.Thread(
        target=distiller_worker,
        args=(state, exit, distill_client),
        daemon=True,
    )
    threads.append(distiller_thread)
    solver_thread = threading.Thread(
        target=solver_worker,
        args=(state, exit, solve_client),
        daemon=True,
    )
    threads.append(solver_thread)
    for thread in threads:
        thread.start()

    try:
        for thread in threads:
            thread.join()
    except KeyboardInterrupt:
        print('\nStopping...')
        exit.set()
        for thread in threads:
            thread.join(timeout=1)
    finally:
        audio.put(None)


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


# Frequently used: uv run utilities/scripts/souffleur.py --distill-model Qwen/Qwen3-8B-GGUF --solve-model Qwen/Qwen3-8B-GGUF --source audio
# Fast alternative: uv run utilities/scripts/souffleur.py --distill-model prism-ml/Bonsai-8B-gguf --solve-model prism-ml/Bonsai-8B-gguf --source audio
# Slow: bartowski/Qwen_Qwen3.6-35B-A3B-GGUF