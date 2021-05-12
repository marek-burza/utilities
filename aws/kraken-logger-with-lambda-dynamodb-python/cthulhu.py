#!/usr/bin/env python3

import boto3
import botocore
import json
import krakenex
import logging
import os
import time

api_key = os.environ['KRAKEN_API_KEY']
private_key = os.environ['KRAKEN_PRIVATE_KEY']

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logging.getLogger('boto3').setLevel(logging.WARNING)
logging.getLogger('botocore').setLevel(logging.WARNING)

def lambda_handler(event, context):
    logger.info('Event: %s' % str(event))

    aws_dynamodb = boto3.client('dynamodb')
    api = krakenex.API(key=api_key, secret=private_key)
    connection = krakenex.Connection()

    now = time.time()
    since = int(now) - 20
    entry = {}
    entry['shard'] = {'S': 'main'}
    entry['stamp'] = {'N': str(now)}
    entry['version'] = {'N': '0'}
    entry['ticker'] = {'S': json.dumps(api.query_public('Ticker', {'pair': 'XXBTZEUR'}))}
    entry['ohlc'] = {'S': json.dumps(api.query_public('OHLC', {'pair': 'XXBTZEUR', 'since': since}))}
    entry['depth'] = {'S': json.dumps(api.query_public('Depth', {'pair': 'XXBTZEUR'}))}
    entry['trades'] = {'S': json.dumps(api.query_public('Trades', {'pair': 'XXBTZEUR', 'since': since}))}
    entry['spread'] = {'S': json.dumps(api.query_public('Spread', {'pair': 'XXBTZEUR', 'since': since}))}

    aws_dynamodb.put_item(TableName='cthulhu', Item=entry)

if __name__ == "__main__":
    lambda_handler({}, {})

# assets = api.query_public('Assets')
# for asset in assets['result']:
#     print(assets['result'][asset])
#
# asset_pairs = api.query_public('AssetPairs')
# for pair in asset_pairs['result']:
#     if pair.endswith('.d'):
#         continue
#     reply = api.query_public('Ticker', {'pair': pair})
#     print('%s %s %s %s' % (pair, str(reply['result'][pair]['a']), str(reply['result'][pair]['b']), str(reply['result'][pair]['v'])))
