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
import logging.handlers
import mimetypes
import os
import random
import sys
import time
import traceback

# Create logger
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
# Create log handler
handler = logging.handlers.SysLogHandler(address=('localhost', 514))
handler.setLevel(logging.INFO)
# Create log formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add the log formatter to handler
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)
# Store the S3 credentials
try:
    identity = os.environ['AWS_ACCESS_KEY_ID'].strip()
    key = os.environ['AWS_SECRET_ACCESS_KEY'].strip()
except:
    logger.error('The application is not configured')
    sys.exit()
with open('/tmp/passwd-s3fs' ,'wb') as passwd:
    passwd.write('%s:%s\n' % (identity, key))
os.system('chmod 400 /tmp/passwd-s3fs')

# Generate a successive file name
def successive():
    stamp = int(time.time() * 1000)
    smear = int(random.random() * 1E20) % 0x10000000000000000
    return '%016X%016X' % (stamp, smear)

# Try to guess the file extension
def extension(mime):
    if mime == None or mime.find('/') == -1:
        return ''
    found = mimetypes.guess_extension(mime)
    if found == None:
        return '.' + mime.split('/')[-1]
    else:
        return found

# Split the path into bucket name and prefix
def locate(path):
    path = path.split('/')
    name = path[0]
    prefix = '/'.join(path[1:])
    if 0 != len(prefix):
        prefix = '%s/' % prefix
    return (name, prefix)

def reply(start_response, code):
    start_response(code, [('Content-Type','text/html')])
    return [b'']

# Handle HTTP requests
def application(environ, start_response):
    if 'POST' != environ.get('REQUEST_METHOD'):
        return reply(start_response, '500 Internal Server Error')
    path = environ.get('PATH_INFO')[1:]
    try:
        (name, prefix) = locate(path)
        if None == name or 0 == len(name):
            logger.error('The requested path was invalid (%s)' % path)
            return reply(start_response, '500 Internal Server Error')
    except:
        logger.error('Failed to parse the path (%s)' % path)
        return reply(start_response, '500 Internal Server Error')
    mime = environ.get('CONTENT_TYPE', 'application/data')
    try:
        length = int(environ.get('CONTENT_LENGTH', 0))
    except:
        length = 0
    body = environ['wsgi.input'].read(length)
    mount = '/mnt/s3/%s' % name
    if not os.path.isdir(mount):
        os.system('mkdir -p %s' % mount)
        os.system('s3fs %s %s -o passwd_file=/tmp/passwd-s3fs' % (name, mount))
        os.system('mkdir -p %s/%s' % (mount, prefix))
    path = '%s/%s%s%s' % (mount, prefix, successive(), extension(mime))
    try:
        with open(path, 'wb') as handle:
            handle.write(body)
        logger.info('Collected %d bytes' % length)
    except:
        logger.error('Failed to create an S3 object:\n%s' % traceback.format_exc())
        return reply(start_response, '500 Internal Server Error')
    return reply(start_response, '200 OK')
