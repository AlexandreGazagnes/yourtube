import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)

prefix = "/video"


class TestIntegrationVideos:
    @pytest.mark.parametrize(
        "id_video,expected",
        [
            ("_URmd_ff8HU", 200),
        ],
    )
    def test_get_video(self, id_video, expected):
        """Test the ping route"""

        response = client.get(f"{prefix}/{id_video}")
        assert response.status_code == expected
        # assert response.json() == {"message": "Hello World"}

        logging.info(response.json())
