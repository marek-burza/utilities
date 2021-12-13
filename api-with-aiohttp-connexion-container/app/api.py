#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the script with API handler functions
"""

import json
import random

import aiohttp.web


async def lottery(request):
    """
    Handles the 'lottery' endpoint
    """
    logger = request.app['LOGGER']
    try:
        request = await request.json()
        logger.info(str(request))
    except RuntimeError as exception:
        logger.exception('Failed to run "lottery"')
        return aiohttp.web.json_response({'error': str(exception)}, status=500)
    result = {'random': random.random()}
    return aiohttp.web.json_response(result, status=200)
