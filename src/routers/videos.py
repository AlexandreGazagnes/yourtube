from fastapi import FastAPI, HTTPException, APIRouter
from src.models import *
from src.queries import query_all

# from src.validators import ChannelBase, default_channel

import logging


videos = APIRouter(
    prefix="/videos",
    tags=["videos"],
)


@videos.get("")
async def get_all_videos():
    return query_all(Categ1)
