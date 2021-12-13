#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the script with the main code of the application
"""

import logging
import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from api import api


app = FastAPI()


@app.get('/', include_in_schema=False)
async def index():
    """
    Redirecting root to index.html
    """
    return RedirectResponse('/index.html')


def go():
    """
    Runs the web server
    """
    app.mount('/api', api)
    app.mount('/', StaticFiles(directory='/app/web', html=True), name='static')

    api.logger = logging.getLogger('app')
    config = uvicorn.config.LOGGING_CONFIG
    del config['loggers']
    uvicorn.run(app, port=80, host='0.0.0.0', log_config=config)



if __name__ == '__main__':
    pattern = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(format=pattern, level=logging.INFO)
    go()
