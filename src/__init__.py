from fastapi import FastAPI

# from src.routers import Router
import logging

from src.categ_1.routers import categ_1
from src.categ_2.routers import categ_2
from src.channels.routers import channels
from src.home.routers import home
from src.languages.routers import languages
from src.status.routers import status

# from src.users.routers import users
# from src.userschannels.routers import userschannels
from src.videos.routers import videos


def create_app():
    """Create a FastAPI app instance"""

    # app
    app = FastAPI()

    # routers
    app.include_router(categ_1)
    app.include_router(categ_2)
    app.include_router(channels)
    app.include_router(home)
    app.include_router(languages)

    app.include_router(status)
    # app.include_router(users)
    # app.include_router(userschannels)
    app.include_router(videos)

    return app


if __name__ != "__main__":
    app = create_app()
    logging.warning("Starting app")
