#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import boto3
import os
import sys

from contextlib import closing


# /Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to pdf *.odp
# convert -density 174.2 *.pdf $(ls *.pdf | sed 's/\.pdf//g').jpg


def silence():
    os.system('ffmpeg -f s16le -ac 1 -t 1 -i /dev/zero -ar 22050 -y silence.mp3')


def what():
    return sys.argv[1]


def which():
    if len(sys.argv) <= 2:
        return None
    return [int(index) for index in sys.argv[2:]]


def fetch(prefix):
    with open('{}.txt'.format(prefix), 'r') as handle:
        return handle.readlines()


def polly():
    session = boto3.Session(region_name='eu-west-1')
    return session.client('polly')


def tts(prefix, aws_polly, lines, index):
    index -= 1
    response = aws_polly.synthesize_speech(
        Text=lines[index], OutputFormat='mp3', VoiceId='Matthew')
    name = '{}.{:03d}.mp3'.format(prefix, index)
    os.system('rm {} 2> /dev/null'.format(name))
    with closing(response['AudioStream']) as handle:
        with open(name, 'wb') as mp3:
            mp3.write(handle.read())


def prepend(prefix, index):
    name_mp3 = '{}.{:03d}.mp3'.format(prefix, index)
    name_aac = '{}.{:03d}.aac'.format(prefix, index)
    template = 'ffmpeg -i concat:"silence.mp3|{}" -strict -2 -y {}'
    os.system(template.format(name_mp3, name_aac))


def mix(prefix, index):
    name_jpg = '{}-{}.jpg'.format(prefix, index)
    name_aac = '{}.{:03d}.aac'.format(prefix, index)
    template = 'ffmpeg -loop 1 -i {} -i {} -strict -2 -crf 25 -c:v libx264 -tune stillimage -pix_fmt yuv420p -shortest -y {}.{:03d}.mp4'
    os.system(template.format(name_jpg, name_aac, prefix, index))


def main():
    prefix = what()
    indices = which()
    lines = fetch(prefix)
    if indices is None:
        indices = range(1, len(lines) + 1)
    silence()
    aws_polly = polly()
    for index in indices:
        tts(prefix, aws_polly, lines, index)
        prepend(prefix, index)
        mix(prefix, index)


if __name__ == '__main__':
    main()
