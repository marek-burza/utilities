#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TODO - replace with:
# - https://github.com/myshell-ai/MeloTTS
# - https://huggingface.co/coqui/XTTS-v2
# - https://github.com/SWivid/F5-TTS
# - https://github.com/SparkAudio/Spark-TTS

import boto3
import os
import sys

from contextlib import closing


# soffice --headless --convert-to pdf *.odp
# convert -density 174.2 *.pdf $(ls *.pdf | sed 's/\.pdf//g').jpg


def silence():
    #os.system('ffmpeg -f s16le -ac 1 -t 1 -i /dev/zero -ar 22050 -y silence.mp3')
    os.system('ffmpeg -f lavfi -i anullsrc=channel_layout=mono:sample_rate=22050 -t 1 -y silence.flac')


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
    response = aws_polly.synthesize_speech(
        Text=lines[index], OutputFormat='mp3', VoiceId='Matthew')
    name = '{}.{:03d}.mp3'.format(prefix, index)
    os.system('rm {} 2> /dev/null'.format(name))
    with closing(response['AudioStream']) as handle:
        with open(name, 'wb') as mp3:
            mp3.write(handle.read())


def flac(prefix, index):
    name_mp3 = '{}.{:03d}.mp3'.format(prefix, index)
    name_flac = '{}.{:03d}.flac'.format(prefix, index)
    template = 'ffmpeg -i {} -y {}'
    command = template.format(name_mp3, name_flac)
    os.system(command)
    os.system('rm {}'.format(name_mp3))


def prepend(prefix, index):
    name_flac = '{}.{:03d}.flac'.format(prefix, index)
    name_ok = '{}.{:03d}.ok.mp3'.format(prefix, index)
    template = 'ffmpeg -i concat:"silence.flac|{}" -y {}'
    command = template.format(name_flac, name_ok)
    os.system(command)
    os.system('rm {}'.format(name_flac))


def mix(prefix, index):
    name_jpg = '{}-{}.jpg'.format(prefix, index)
    name_ok = '{}.{:03d}.ok.mp3'.format(prefix, index)
    template = 'ffmpeg -loop 1 -i {} -i {} -crf 25 -c:v libx264 -tune stillimage -pix_fmt yuv420p -shortest -y {}.{:03d}.mp4'
    command = template.format(name_jpg, name_ok, prefix, index)
    os.system(command)
    os.system('rm {}'.format(name_ok))


def main():
    prefix = what()
    indices = which()
    lines = fetch(prefix)
    if indices is None:
        indices = range(len(lines))
    silence()
    aws_polly = polly()
    for index in indices:
        tts(prefix, aws_polly, lines, index)
        flac(prefix, index)
        prepend(prefix, index)
        mix(prefix, index)


if __name__ == '__main__':
    main()
