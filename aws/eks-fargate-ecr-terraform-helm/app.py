#!/usr/bin/env python3

import logging
import uvicorn

from fastapi import FastAPI, Response, status


logging.basicConfig(
    format='%(asctime)s %(levelname)s %(name)s %(message)s',
    level=logging.DEBUG)
logger = logging.getLogger('example')


app = FastAPI()


@app.get('/')
async def root():
    return Response(status_code=status.HTTP_200_OK)


if __name__ == '__main__':
    config = uvicorn.config.LOGGING_CONFIG
    del config['loggers']
    uvicorn.run(app, port=80, host='0.0.0.0', log_config=config)
