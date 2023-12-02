import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)


class TestUsers:
    """Test the users routes"""

    def test_users_counts(self):
        """Test the get users route"""

        response = client.get("/users/counts")
        # assert response.status_code == 200
        # assert len(response.json()) > 0

        logging.warning(response.json())

    def test_users_preferences(self, id_user=3):
        """Test the get users route"""

        response = client.get(f"/users/preferences", params={"id_user": id_user})
        assert response.status_code == 200
        # assert len(response.json()) > 0

        json = response.json()
        assert len(json.keys())
        assert len(json["payload"].keys())
        logging.warning(response.json())
