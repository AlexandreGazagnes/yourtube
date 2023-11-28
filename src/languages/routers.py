from fastapi import FastAPI, HTTPException, APIRouter
from src.models.db import *
from src.queries import query_all
from src.routers.helpers import jsonify


# from src.validators import ChannelBase, default_channel

import logging

languages = APIRouter(
    prefix="/languages",
    tags=["languages"],
)


@languages.get("")
async def get_all_languages():
    return jsonify(query_all(Language))

