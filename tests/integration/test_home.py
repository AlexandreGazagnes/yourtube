import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)


class TestHome:
    """Test the home routes"""

    def test_ping(self):
        """Test the ping route"""

        response = client.get("/ping")
        # assert response.status_code == 200
        # assert response.json() == {"message": "Hello World"}

        logging.warning(response.json())
