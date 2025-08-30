#!/usr/bin/env -S uv run --script --quiet
# -*- coding: utf-8 -*-
# /// script
# requires-python = "<=3.10"
# dependencies = [
#     "parler-tts",
#     "scipy",
#     "torch",
#     "torchaudio",
# ]
#
# [tool.uv.sources]
# parler-tts = { git = "https://github.com/huggingface/parler-tts.git" }
# ///
# Inspiration:
# - https://huggingface.co/docs/transformers/en/tasks/text-to-speech
# Other options:
# - https://github.com/hexgrad/kokoro - open-weight TTS model
# - https://github.com/openai/whisper & https://github.com/ggml-org/whisper.cpp - OpenAI speech recognition
# - https://github.com/Uberi/speech_recognition - speech recognition Python package
# - https://github.com/ictnlp/LLaMA-Omni - LLaMA-based speech interaction
# - https://github.com/kyutai-labs/moshi - speech interaction foundation model

import os
import sys
from pathlib import Path
from typing import Any

import torch
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from scipy.io.wavfile import write
from transformers import AutoTokenizer, pipeline, set_seed


set_seed(67)


# https://github.com/huggingface/parler-tts
class TtsParler:
    def __init__(self) -> None:
        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model = ParlerTTSForConditionalGeneration.from_pretrained('parler-tts/parler-tts-mini-v1').to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained('parler-tts/parler-tts-mini-v1')
        description = 'An american male speaker with a deep voice delivers an informative slide narration with a moderate speed. The recording is of very high quality, with the speaker\'s voice sounding clear.'
        self.input_ids = self.tokenizer(description, return_tensors='pt').input_ids.to(self.device)

    def tts(self, text: str) -> tuple[Any, Any]:
        prompt_input_ids = self.tokenizer(text, return_tensors='pt').input_ids.to(self.device)
        generation = self.model.generate(input_ids=self.input_ids, prompt_input_ids=prompt_input_ids)
        audio = generation.cpu().numpy().squeeze()
        rate = self.model.config.sampling_rate
        return (audio, rate)


# https://huggingface.co/docs/transformers/en/model_doc/vits
class TtsVits:
    def __init__(self) -> None:
        self.pipe = pipeline(
            task='text-to-speech',
            model='facebook/mms-tts-eng',
        )

    def tts(self, text: str) -> tuple[Any, Any]:
        output = self.pipe(text)
        audio = output['audio'].squeeze()
        rate = output['sampling_rate']
        return (audio, rate)


def audio_scipy(audio: Any, rate: Any, path: Path) -> None:
    sf.write(path, audio, rate)


def audio_soundfile(audio: Any, rate: Any, path: Path) -> None:
    write(path, rate, audio)


def silence():
    os.system('ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -t 1 -y silence.flac')


def what() -> str:
    return sys.argv[1]


def which() -> list[int]:
    if len(sys.argv) <= 2:
        return []
    return [int(index) for index in sys.argv[2:]]


def fetch(prefix: str) -> list[str]:
    with open(f'{prefix}.txt', 'r') as handle:
        return handle.readlines()


def speech(prefix: str, tts: Any, lines: list[str], index: int) -> None:
    name = f'{prefix}.{index:02d}.wav'
    path = Path(name)
    text = lines[index].strip()
    if len(text) > 0:
        if path.exists():
            path.unlink()
        audio, rate = tts.tts(text)
        audio_soundfile(audio, rate, path)


def flac(prefix: str, index: int) -> None:
    name_wav = f'{prefix}.{index:02d}.wav'
    name_flac = f'{prefix}.{index:02d}.flac'
    command = f'ffmpeg -i {name_wav} -ar 44100 -ac 2 -sample_fmt s16 -y {name_flac}'
    os.system(command)


def prepend(prefix: str, index: int) -> None:
    name_flac = f'{prefix}.{index:02d}.flac'
    name_ok = f'{prefix}.{index:02d}.ok.flac'
    command = f'ffmpeg -i concat:"silence.flac|{name_flac}" -y {name_ok}'
    os.system(command)


def mix(prefix: str, index: int) -> None:
    name_png = f'{prefix}.{index:02d}.png'
    name_ok = f'{prefix}.{index:02d}.ok.flac'
    command = f'ffmpeg -loop 1 -i {name_png} -i {name_ok} -crf 25 -c:v libx264 -tune stillimage -pix_fmt yuv420p -shortest -y {prefix}.{index:02d}.mp4'
    os.system(command)


def main() -> None:
    prefix = what()
    indices = which()
    lines = fetch(prefix)
    if not indices:
        indices = range(len(lines))
    silence()
    tts = TtsVits()
    for index in indices:
        speech(prefix, tts, lines, index)
        flac(prefix, index)
        prepend(prefix, index)
        mix(prefix, index)


if __name__ == '__main__':
    main()
