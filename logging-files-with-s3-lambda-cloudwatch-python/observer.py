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

import boto3
import botocore
import configuration
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

def lambda_handler(event, context):
    logger.info('Event: %s' % str(event))
    logger.info('S3 bucket: %s' % configuration.bucket)
    session = boto3.session.Session()
    s3 = session.resource('s3')
    bucket = s3.Bucket(configuration.bucket)
    try:
        s3.meta.client.head_bucket(Bucket=configuration.bucket)
    except botocore.exceptions.ClientError as exception:
        if 404 == int(exception.response['Error']['Code']):
            logger.error('S3 bucket is not available')
            return
    if not event.has_key('Records'):
        logger.error('Malformed event')
        return
    for it in event['Records']:
        if it.has_key('s3'):
            key = it['s3']['object']['key']
            thing = s3.Object(bucket.name, key)
            logging.info('Got object %s:\n%s' % (key, str(bytearray(thing.get()['Body'].read()))))
