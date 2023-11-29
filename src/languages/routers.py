import logging

from fastapi import FastAPI, HTTPException, APIRouter

from src.languages.models import Language
from src.helpers.queries import query_all
from src.helpers.routers import jsonify


languages = APIRouter(
    prefix="/languages",
    tags=["languages"],
)


@languages.get("")
async def get_all_languages():
    """Get all languages"""

    payload = query_all(Language)
    return jsonify(payload=payload, message="done")
