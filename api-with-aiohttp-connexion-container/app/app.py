#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the script with the main code of the application
"""

import json
import logging

import aiohttp.web
import connexion


async def index(request):
    """
    Redirecting root to index.html
    """
    raise aiohttp.web.HTTPFound('/index.html')


def go():
    """
    Runs the web server
    """
    app = connexion.AioHttpApp(
        __name__, port=80, specification_dir='/app/web')

    context_name = 'request'
    api = app.add_api(  # nosec
        'api.yaml',
        base_path='/api',
        options={'swagger_ui': False},
        pass_context_arg_name=context_name)
    api.subapp['LOGGER'] = logging.getLogger('app')

    app.app.router.add_route('*', '/', index)
    app.app.router.add_static(prefix='/', path='/app/web/')

    app.run()


if __name__ == '__main__':
    pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.INFO)
    go()
