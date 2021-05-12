#!/usr/bin/env python

import boto3
import config
import logging
import traceback

# Preparation of logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

# Handler for the requests
def lambda_handler(event, context):
    try:
        logger.info(str(event))
        aws_s3 = boto3.client('s3')
        bucket = config.bucket
        key = config.key
        return aws_s3.get_object(Bucket=bucket, Key=key)['Body'].read()
    except:
        logger.error(traceback.format_exc().replace('\n', '; '))
        return ''
