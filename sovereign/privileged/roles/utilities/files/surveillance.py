#!/usr/bin/env -S uv run --script --quiet
# -*- coding: utf-8 -*-
# /// script
# requires-python = "<=3.10"
# dependencies = [
#     "typer",
# ]
# ///

import subprocess
import typer


def main(
    device: str = typer.Option(
        '/dev/video0',
        '--video',
        '-v',
        help='Video capture device (default: /dev/video0).',
    ),
    scene: float = typer.Option(
        0.01,
        '--scene',
        '-s',
        help='Scene change threshold. Lower values are more sensitive (default: 0.01).',
    ),
    duration: int = typer.Option(
        30,
        '--duration',
        '-d',
        help='Duration of each segment in seconds (default: 30).',
    ),
    filename: str = typer.Option(
        'surveillance_%08d.avi',
        '--template',
        '-t',
        help='Output filename template (default: surveillance_%08d.avi).',
    ),
):
    ffmpeg = [
        'ffmpeg',
        '-f', 'v4l2',
        '-i', device,
        '-vf', f'select=\'gt(scene,{scene})\',setpts=N/FRAME_RATE/TB',
        '-c:v', 'mjpeg',
        '-f', 'segment',
        '-reset_timestamps', '1',
        '-segment_time', str(duration),
        filename,
    ]
    subprocess.run(ffmpeg, shell=False)


if __name__ == '__main__':
    typer.run(main)
