import logging

from fastapi import FastAPI, HTTPException, APIRouter

from src.helpers.queries import query_all
from src.helpers.routers import jsonify
from src.categ_2.models import Categ2

# from src.db import Db
# from src.validators import ChannelBase, default_channel


categ_2 = APIRouter(
    prefix="/categ_2",
    tags=["categ_2"],
)


@categ_2.get("")
async def get_all_categ_2():
    """Get all categ_2"""

    payload = query_all(Categ2)
    return jsonify(payload=payload, message="done")
