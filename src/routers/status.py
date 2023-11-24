from fastapi import FastAPI, HTTPException, APIRouter
from src.models.db import *
from src.queries import query_all
from src.routers.helpers import jsonify


# from src.validators import ChannelBase, default_channel

import logging

status = APIRouter(
    prefix="/status",
    tags=["status"],
)


@status.get("")
async def get_all_status():
    return jsonify(query_all(Status))
