import logging

from fastapi import FastAPI, HTTPException, APIRouter

from src.helpers.queries import query_all
from src.helpers.routers import jsonify

from src.status.models import Status


status = APIRouter(
    prefix="/status",
    tags=["status"],
)


@status.get("")
async def get_all_status():
    """Get all status"""

    payload = query_all(Status)
    return jsonify(payload=payload, message="done")
