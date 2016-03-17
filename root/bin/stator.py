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

import boto3
import logging
import logging.handlers
import os
import stator_configuration

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
# Connect to the queue
aws_sqs = boto3.resource('sqs') #aws_session.resource('sqs')
aws_queue = aws_sqs.get_queue_by_name(QueueName=stator_configuration.aws_queue)
# Process tasks from the queue
while True:
    for message in aws_queue.receive_messages():
        logger.info(message.body)
        try:
            os.system(message.body)
        except:
            logger.error(traceback.format_exc())
        message.delete()
