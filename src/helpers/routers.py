import os
from dotenv import dotenv_values
from fastapi import HTTPException, status, Depends
from src.params import get_params


def jsonify(payload, message="success", total=-1, status=200):
    """jsonify a payload"""

    n = -1 if not isinstance(payload, list) else len(payload)
    return {
        "payload": payload,
        "message": message,
        "status": status,
        "count": n,
        "total": total,
    }


# def token_required(f):
#     # @wraps(f)
#     async def decorated_function(*args, **kwargs):
#         token = kwargs.get("token", None)
#         params = dotenv_values(".env/.env.dev")
#         good_token = params.get("API_TOKEN", None)

#         if token != good_token:
#             raise HTTPException(
#                 status_code=status.HTTP_401_UNAUTHORIZED,
#                 detail="Invalid authentication credentials",
#                 headers={"WWW-Authenticate": "Bearer"},
#             )
#         return await f(*args, **kwargs)

#     return decorated_function


def validate_token(token: str):
    """verify token"""

    params = get_params(os.getenv("MODE", "dev"))
    good_token = params.get("API_TOKEN", None)

    if not good_token:
        raise ValueError("API_TOKEN is not defined")

    if token != good_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token

