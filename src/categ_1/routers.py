import logging

from fastapi import FastAPI, HTTPException, APIRouter

from src.helpers.queries import query_all
from src.helpers.routers import jsonify
from src.categ_1.models import Categ1

# from src.db import Db
# from src.validators import ChannelBase, default_channel


categ_1 = APIRouter(
    prefix="/categ_1",
    tags=["categ_1"],
)


@categ_1.get("")
async def get_all_categ_1():
    """Get all categ_1"""

    payload = query_all(Categ1)
    return jsonify(payload=payload, message="done")
