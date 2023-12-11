import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)


class TestIntegrationUser:
    """Test the users routes"""

    def test_users_preferences(self, id_user=3):
        """Test the get users route"""

        response = client.get(f"/user/preferences", params={"id_user": id_user})
        assert response.status_code == 200
        # assert len(response.json()) > 0

        json = response.json()
        assert len(json.keys())
        assert len(json["payload"].keys())
        logging.info(response.json())
