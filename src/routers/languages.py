from fastapi import FastAPI, HTTPException, APIRouter
from src.models import *
from src.queries import query_all

# from src.validators import ChannelBase, default_channel

import logging

languages = APIRouter(
    prefix="/languages",
    tags=["languages"],
)


@languages.get("")
async def get_all_languages():
    return query_all(Language)
