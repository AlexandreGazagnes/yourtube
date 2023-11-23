from fastapi import FastAPI, HTTPException, APIRouter
from src.models import *
from src.queries import query_all

# from src.validators import ChannelBase, default_channel

import logging


home = APIRouter(
    prefix="",
    tags=["home"],
)


@home.get("/", status_code=200)
async def root():
    return {"message": "Hello World"}
