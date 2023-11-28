from fastapi import FastAPI, HTTPException, APIRouter
from src.models.db import *
from src.queries import query_all
from src.routers.helpers import jsonify

# from src.validators import ChannelBase, default_channel

import logging

categ_1 = APIRouter(
    prefix="/categ_1",
    tags=["categ_1"],
)


@categ_1.get("")
async def get_all_categ_1():
    return jsonify(query_all(Categ1))

