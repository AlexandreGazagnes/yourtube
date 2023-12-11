import logging

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)

prefix = "/user"


class TestIntegrationUser:
    """Test the users routes"""

    @pytest.mark.parametrize("id_user,expected", [3])
    def test_users_preferences(self, id_user):
        """Test the get users route"""

        response = client.get(f"{prefix}/preferences", params={"id_user": id_user})
        assert response.status_code == 200
        # assert len(response.json()) > 0

        json = response.json()
        assert len(json.keys())
        assert len(json["payload"].keys())
        logging.info(response.json())
