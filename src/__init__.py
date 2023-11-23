from fastapi import FastAPI
from src.routers import Router
import logging


def create_app():
    """Create a FastAPI app instance"""

    app = FastAPI()
    app.include_router(Router.home)
    app.include_router(Router.languages)
    app.include_router(Router.categ_1)
    app.include_router(Router.videos)
    app.include_router(Router.channels)

    return app


if __name__ != "__main__":
    app = create_app()
    logging.warning("Starting app")
