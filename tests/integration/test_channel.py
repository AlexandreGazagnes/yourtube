import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)

prefix = "/channel"

test_existing_channel = "test_2492068e"
test_non_existing_channel = "test_24920dezezdezdzeddzedz68e"

true_channel = "UC-06IzcwOHu9_Xgqr-NMkUQ"  # yann leonardi


class TestChannel:
    @pytest.mark.parametrize(
        "id_channel,expected",
        [
            (true_channel, 200),
        ],
    )
    def test_get_channel(self, id_channel, expected):
        """Test the ping route"""

        response = client.get(f"{prefix}/{id_channel}")
        assert response.status_code == expected
        # assert response.json() == {"message": "Hello World"}

        logging.info(response.json())
