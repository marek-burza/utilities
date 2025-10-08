#!/usr/bin/env -S uv run --script --quiet
# -*- coding: utf-8 -*-
# /// script
# requires-python = "<=3.10"
# dependencies = [
#     "typer",
# ]
# ///

import re
import subprocess
from pathlib import Path

import typer


def main(
    path: Path = typer.Option(
        ...,
        '--path',
        '-p',
        help='Path to image directory.',
    ),
    title: Path = typer.Option(
        ...,
        '--title',
        '-t',
        help='Title of the image album.',
    ),
):
    for item in path.iterdir():
        if item.is_file():
            command = [
                'identify',
                '-format',
                '%[EXIF:DateTimeOriginal]',
                item,
            ]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            stamp = re.sub(r'\D', '', result.stdout.strip())
            stem = f'{title}.{stamp}'
            suffix = item.suffix.lower()
            name = f'{stem}{suffix}'
            item.rename(item.with_name(name))


if __name__ == '__main__':
    typer.run(main)
