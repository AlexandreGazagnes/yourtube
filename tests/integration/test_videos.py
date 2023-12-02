import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)


prefix = "/videos"


class TestVideos:
    """Test the videos routes"""

    # def get_all_videos(self):
    #     """Test the get videos route"""

    #     # response = client.get(f"{prefix}")
    #     # assert response.status_code == 200
    #     # assert len(response.json()) > 0

    #     # logging.warning(response.json())

    def videos_counts(self):
        """Test the get videos route"""

        response = client.get(f"{prefix}/counts")
        # # assert response.status_code == 200
        # # assert len(response.json()) > 0

        # logging.warning(response.json())

    # def test_videos(self):
    #     """Test the get videos route all"""

    #     response = client.get(f"{prefix}")
    #     assert response.status_code == 200
    #     # assert len(response.json()) > 0

    #     payload = response.json()
    #     assert len(payload)

    #     logging.warning(response.json())

    @pytest.mark.parametrize(
        "params",
        [
            ({"id_user": 3}),
            ({"id_user": 3, "query": "psg"}),
            ({"id_user": 3, "id_language": "En"}),
        ],
    )
    def test_get_videos_by_user(
        self,
        params: dict | None,
    ) -> dict:
        """Test the get videos route by user"""

        response = client.get(f"{prefix}/by_user", params=params)
        assert response.status_code == 200
        # assert len(response.json()) > 0

        logging.warning(response.json())
