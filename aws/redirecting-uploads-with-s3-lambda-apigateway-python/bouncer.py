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
import random
import time

# Generate a successive file name
def successive():
    stamp = int(time.time() * 1000)
    smear = int(random.random() * 1E20) % 0x10000000000000000
    return '%016X%016X' % (stamp, smear)

# Prepare logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

# Handle requests
def lambda_handler(event, context):
    logger.info('Event: %s' % str(event))
    s3 = boto3.client('s3')
    parameters = {
        'ACL': 'authenticated-read',
        'Bucket': configuration.bucket,
        'Key': successive()
        }
    url = s3.generate_presigned_url(
        'put_object', Params=parameters, ExpiresIn=3600
        )
    return {'location': url}
