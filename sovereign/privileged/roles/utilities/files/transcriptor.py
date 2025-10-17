#!/usr/bin/env -S uv run --script --quiet
# -*- coding: utf-8 -*-
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "accelerate",
#     "torch",
#     "transformers",
#     "typer",
# ]
# ///
# Inspiration:
# - https://huggingface.co/openai/whisper-large-v3

from pathlib import Path

import torch
import typer
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline


def main(
    input_path: Path = typer.Option(
        ...,
        '--input-path',
        '-i',
        help='Path to input audio file.',
    ),
    output_path: Path = typer.Option(
        ...,
        '--output-path',
        '-o',
        help='Path to output transcription file.',
    ),
) -> None:
    device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model_id = 'openai/whisper-large-v3'
    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)
    processor = AutoProcessor.from_pretrained(model_id)
    pipe = pipeline(
        'automatic-speech-recognition',
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        dtype=torch_dtype,
        device=device,
        return_timestamps=True,
    )
    result = pipe(str(input_path))
    with output_path.open('wt') as handle:
        handle.write(result['text'])


if __name__ == '__main__':
    typer.run(main)
