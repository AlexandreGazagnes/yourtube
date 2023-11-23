from fastapi import FastAPI

from src.models import *


def create_app():
    """Create a FastAPI app instance"""

    app = FastAPI()

    @app.get("/")
    async def root():
        return {"message": "Hello World"}

    # @app.get("/items/{item_id}")
    # async def read_item(item_id):
    #     return {"item_id": item_id}

    def add_channel(channel):
        """ """
        pass

    def update_channel(channel):
        """ """
        pass

    def update_videos(videos):
        """ """
        pass

    def get_all_videos():
        pass

    def get_all_channels():
        pass

    def get_all_categ1():
        pass

    @app.get("/languages/")
    async def get_all_languages():
        """get all languages"""

        with Session(engine) as session:
            result = session.execute(select(Language)).all()

            json = [row.serialize() for row in result]
            return json

    return app
