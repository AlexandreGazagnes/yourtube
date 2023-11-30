import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)


class TestVideos:
    """Test the videos routes"""

    # def get_all_videos(self):
    #     """Test the get videos route"""

    #     # response = client.get("/videos")
    #     # assert response.status_code == 200
    #     # assert len(response.json()) > 0

    #     # logging.warning(response.json())

    def videos_counts(self):
        """Test the get videos route"""

        response = client.get("/videos/counts")
        # # assert response.status_code == 200
        # # assert len(response.json()) > 0

        # logging.warning(response.json())

    @pytest.mark.parametrize(
        "id_user,params",
        [
            (3, {}),
            (3, {"query": "psg"}),
            (3, {"id_language": "En"}),
        ],
    )
    def test_get_videos_by_user(
        self,
        id_user: int,
        params: dict | None,
    ) -> dict:
        """Test the get videos route"""

        response = client.get(f"/videos/by_user/{id_user}", params=params)
        # assert response.status_code == 200
        # assert len(response.json()) > 0

        logging.warning(response.json())
