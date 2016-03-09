#!/usr/bin/python

# This code is free software: you can redistribute it and/or modify it under the
# terms  of  the  GNU Lesser General Public License  as published  by  the  Free
# Software Foundation,  either version 3 of the License, or (at your option) any
# later version.
#
# This code is distributed in the hope that it will be useful,  but  WITHOUT ANY
# WARRANTY;  without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A  PARTICULAR  PURPOSE.  See  the  GNU Lesser General Public License  for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with code. If not, see http://www.gnu.org/licenses/.

import logging
import logging.handlers
import mimetypes
import os
import random
import sys
import time
import traceback

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create log handler
LOG_FILE = '/tmp/simple-collector.log'
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
with open('/etc/s3fs.passwd' ,'wb') as passwd:
    passwd.write('%s:%s\n' % (identity, key))
os.system('chmod 600 /etc/s3fs.passwd')

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
        os.system('s3fs %s %s -o passwd_file=/etc/s3fs.passwd' % (name, mount))
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
