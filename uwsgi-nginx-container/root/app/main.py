#!/usr/bin/env python3

import sys

def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello from Python %s' % sys.version.encode('utf-8')]
