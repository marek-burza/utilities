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
import flask
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

# Create the Flask app
app = flask.Flask(__name__)

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

@app.route('/', methods=['GET'])
def health():
    return ''

# Handle HTTP requests
@app.route('/', defaults={'path': ''}, methods=['POST'])
@app.route('/<path:path>', methods=['POST'])
def collect(path):
    mime = flask.request.headers.get('Content-Type')
    body = flask.request.data
    try:
        (name, prefix) = locate(path)
        if None == name or 0 == len(name):
            logger.error('The requested path was invalid (%s)' % path)
            return ''
    except:
        logger.error('Failed to parse the path (%s)' % path)
        return ''
    try:
        s3_id     = os.environ['AWS_ACCESS_KEY_ID']
        s3_key    = os.environ['AWS_SECRET_ACCESS_KEY']
        s3_region = os.environ['AWS_DEFAULT_REGION']
    except:
        logger.error('The application is not configured')
        return
    try:
        session = boto3.session.Session(aws_access_key_id=s3_id, aws_secret_access_key=s3_key, region_name=s3_region)
        s3 = session.resource('s3')
        bucket = s3.Bucket(name)
    except:
        logger.error('Failed to establish S3 session:\n%s' % traceback.format_exc())
        return ''
    try:
        s3.meta.client.head_bucket(Bucket=name)
    except:
        logger.error('Failed to access the S3 bucket (%s):\n%s' % (name, traceback.format_exc()))
    try:
        bucket.put_object(Key='%s%s%s' % (prefix, successive(), extension(mime)), Body=body)
    except:
        logger.error('Failed to create an S3 object:\n%s' % traceback.format_exc())
    return ''

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0')
