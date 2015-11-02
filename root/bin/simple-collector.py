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

import boto3
import botocore
import logging
import logging.handlers
import mimetypes
import os
import random
import time
import traceback

# Create logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# Create log handler
LOG_FILE = '/tmp/simple-collector.log'
handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1048576, backupCount=5)
handler.setLevel(logging.INFO)
# Create log formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Add the log formatter to handler
handler.setFormatter(formatter)
# Add the handler to the logger
logger.addHandler(handler)

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

# Handle HTTP requests
def application(environ, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    if 'POST' != environ.get('REQUEST_METHOD'):
        return [b'']
    path = environ.get('PATH_INFO')[1:]
    try:
        (name, prefix) = locate(path)
        if None == name or 0 == len(name):
            logger.error('The requested path was invalid (%s)' % path)
            return [b'']
    except:
        logger.error('Failed to parse the path (%s)' % path)
        return [b'']
    mime = environ.get('CONTENT_TYPE', 'application/data')
    try:
        length = int(environ.get('CONTENT_LENGTH', 0))
    except:
        length = 0
    body = environ['wsgi.input'].read(length)
    try:
        s3_id     = os.environ['AWS_ACCESS_KEY_ID'].strip()
        s3_key    = os.environ['AWS_SECRET_ACCESS_KEY'].strip()
        s3_region = os.environ['AWS_DEFAULT_REGION'].strip()
    except:
        logger.error('The application is not configured')
        return [b'']
    try:
        session = boto3.session.Session(aws_access_key_id=s3_id, aws_secret_access_key=s3_key, region_name=s3_region)
        s3 = session.resource('s3')
        bucket = s3.Bucket(name)
    except:
        logger.error('Failed to establish S3 session:\n%s' % traceback.format_exc())
        return [b'']
    try:
        s3.meta.client.head_bucket(Bucket=name)
    except botocore.exceptions.ClientError as exception:
        if 404 == int(exception.response['Error']['Code']):
            logger.error('Failed to access the S3 bucket (%s):\n%s' % (name, traceback.format_exc()))
            return [b'']
    try:
        bucket.put_object(Key='%s%s%s' % (prefix, successive(), extension(mime)), Body=body)
        logger.info('Collected %d bytes' % length)
    except:
        logger.error('Failed to create an S3 object:\n%s' % traceback.format_exc())
    return [b'']
