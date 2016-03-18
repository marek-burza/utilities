#!/usr/bin/python
#
# The MIT License (MIT)
#
# Copyright (c) 2016
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import os
import subprocess
import sys
import threading

class Filter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR

def add_file_handler(logger, path):
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    try:
        os.remove(path)
    except:
        pass
    handler = logging.FileHandler(path)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    logger.addHandler(handler)

def add_stream_handler(logger):
    formatter = logging.Formatter('%(message)s')
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    handler.setLevel(logging.ERROR)
    logger.addHandler(handler)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.setLevel(logging.DEBUG)
    handler.addFilter(Filter())
    logger.addHandler(handler)

def logger(tag, path=None):
    logger = logging.getLogger(tag)
    logger.setLevel(logging.DEBUG)
    if path != None:
        add_file_handler(logger, path)
    else:
        add_stream_handler(logger)
    return logger

class Tunnel(threading.Thread):
    def __init__(self, pipe, lock, log):
        threading.Thread.__init__(self)
        self.pipe = pipe
        self.lock = lock
        self.log = log

    def run(self):
        with self.pipe:
            for line in iter(self.pipe.readline, b''):
                self.lock.acquire()
                self.log(line.strip())
                self.lock.release()

def execute(command, logger):
    chain = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1)
    lock = threading.Lock()
    stdout = Tunnel(chain.stdout, lock, logger.info)
    stdout.start()
    stderr = Tunnel(chain.stderr, lock, logger.error)
    stderr.start()
    chain.wait()
