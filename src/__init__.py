from fastapi import FastAPI

# from src.routers import Router
import logging

logging.basicConfig(
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s - %(levelname)s - %(pathname)s- %(funcName)s - %(lineno)d :\n %(message)s\n",
    datefmt="'%Y-%m-%d %H:%M:%S.",
)

# FORMAT="%(asctime)s %(clientip)-15s %(user)-8s %(message)s",
# handlers=[logging.StreamHandler()],,
# formatter = logging.Formatter(
#     "[%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s",
#     "%m-%d %H:%M:%S",
# )
from src.categ_1.routers import categ_1
from src.categ_2.routers import categ_2
from src.channels.routers import channels, channel
from src.home.routers import home
from src.languages.routers import languages
from src.status.routers import status
from src.users.routers import users, user

# from src.users.routers import users
# from src.userschannels.routers import userschannels
from src.videos.routers import videos, video


def create_app():
    """Create a FastAPI app instance"""

    # app
    app = FastAPI()

    # routers
    app.include_router(categ_1)
    app.include_router(categ_2)

    app.include_router(channel)
    app.include_router(channels)

    app.include_router(home)

    app.include_router(languages)
    app.include_router(status)

    app.include_router(user)
    app.include_router(users)

    app.include_router(video)
    app.include_router(videos)

    # app.include_router(userschannels)

    return app


if __name__ != "__main__":
    app = create_app()
    logging.warning("Starting app")
