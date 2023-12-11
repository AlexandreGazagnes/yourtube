import logging, time, random

from fastapi import FastAPI, HTTPException, APIRouter, Depends

# from src.db import Channel, Video, session, engine, Session
from src.helpers.routers import jsonify, validate_token  # token_required
from src.helpers.queries import query_all

from src.users.queries import UserQuery, UsersQueries

# from src.queries import query_all, jsonify
# from src.validators import ChannelBase, default_channel
# import pandas as pd

# from src.videos.models import Video
# logging.basicConfig(level=logging.INFO)


####################################
#   USER
####################################

user = APIRouter(
    prefix="/user",
    tags=["user"],
)


@user.get("/preferences", status_code=200)
async def get_user_preferences(
    id_user: int | None = 3,
):
    """get user preferences from db and return as json"""

    payload = UserQuery.get_preferences(id_user=id_user)

    return jsonify(payload, message="done")


###################################
#   USERS
###################################


users = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users.get("/counts", status_code=200)
async def get_users_counts():
    """counts users in"""

    payload = UsersQueries.count()
    return jsonify(payload, message="done")
