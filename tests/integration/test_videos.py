import logging
from pprint import pprint, pformat

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)


prefix = "/videos"


class TestVideos:
    """Test the videos routes"""

    def get_all(self):
        """Test the get videos route"""

        response = client.get(f"{prefix}")
        assert response.status_code == 200
        assert len(response.json()) > 0
        video_list = response.json()["videos"]
        assert len(video_list) > 0

        logging.info(pformat(video_list[:5]))

    # def videos_counts(self):
    #     """Test the get videos route"""

    #     response = client.get(f"{prefix}/counts")
    #     # # assert response.status_code == 200
    #     # # assert len(response.json()) > 0

    #     # logging.info(response.json())

    @pytest.mark.parametrize(
        "params",
        [
            ({"id_user": 3}),
            ({"id_user": 3, "query": "psg"}),
            ({"id_user": 1, "id_language": "En"}),
            ({"id_user": 1, "id_categ_1": "Misc."}),
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

        video_list = response.json()["videos"]
        logging.info(pformat(video_list[:5]))

    @pytest.mark.parametrize(
        "params",
        [
            ({"id_channel": "UCENv8pH4LkzvuSV_qHIcslg", "days_max": 100}),
        ],
    )
    def test_get_videos_by_channel(
        self,
        params: dict | None,
    ) -> dict:
        """Test the get videos route by user"""

        response = client.get(f"{prefix}/by_channel", params=params)
        assert response.status_code == 200
        # assert len(response.json()) > 0

        video_list = response.json()["videos"]
        logging.info(pformat(video_list[:5]))
