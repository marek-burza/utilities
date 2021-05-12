#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging

import numpy

from flask import Flask, request


app = Flask(__name__)


@app.route('/api/generate')
def generate():
    logging.info(str(request))
    try:
        with open('/data/date.txt', 'rb') as handle:
            data = handle.read().decode('utf-8')
    except:
        data = None
    response = {'value': numpy.random.random(), 'data': data}
    response = json.dumps(response)
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
