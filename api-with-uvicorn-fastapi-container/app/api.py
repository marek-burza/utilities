#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is the script with API handler functions
"""

import random

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


class LotteryRequest(BaseModel):
    parameter: str


class LotteryReply(BaseModel):
    random: float


api = FastAPI(title='API', version='api')


@api.post('/lottery', summary='Lottery', openapi_extra={'requestBody': {'description': 'Lottery request'}}, response_description='Lottery reply', response_model=LotteryReply, status_code=200)
async def lottery(request: LotteryRequest):
    """
    Handles the 'lottery' endpoint
    """
    logger = api.logger
    try:
        logger.info(str(request))
        if request.parameter == 'crash':
            raise Exception('Must crash')
    except RuntimeError as exception:
        logger.exception('Failed to run "lottery"')
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exception))
    return LotteryReply(random=random.random())
