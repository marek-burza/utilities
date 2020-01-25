#!/usr/bin/env python3

import json
import logging

import azure.functions
import numpy


def main(request: azure.functions.HttpRequest) -> azure.functions.HttpResponse:
    logging.info(str(request))
    with open('/data/date.txt', 'rb') as handle:
        data = handle.read().decode('utf-8')
    response = {'value': numpy.random.random(), 'data': data}
    response = json.dumps(response)
    return azure.functions.HttpResponse(
        response,
        mimetype='application/json', status_code=200)
