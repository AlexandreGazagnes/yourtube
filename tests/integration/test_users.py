import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)

prefix = "/users"


class TestIntegrationUsers:
    """Test the users routes"""

    def test_users_counts(self):
        """Test the get users route"""

        response = client.get(f"{prefix}/counts")
        # assert response.status_code == 200
        # assert len(response.json()) > 0

        logging.warning(response.json())
