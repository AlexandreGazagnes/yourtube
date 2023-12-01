import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)

prefix = "/channels"


class TestChannels:
    def test_get_channels(self):
        """Test the ping route"""

        response = client.get(prefix)
        assert response.status_code == 200
        # assert response.json() == {"message": "Hello World"}

        logging.warning(response.json())
