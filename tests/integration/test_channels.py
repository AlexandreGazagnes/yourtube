import logging
from pprint import pprint, pformat

# Import TestClient and your FastAPI app
from fastapi.testclient import TestClient
from src import app
import pytest


client = TestClient(app)

prefix = "/channels"


class TestIntergationChannels:
    """TestChannels"""

    def test_get_channels(self):
        """Test the ping route"""

        #         response = client.get(prefix)
        #         assert response.status_code == 200
        #         # assert response.json() == {"message": "Hello World"}

        #         logging.info(response.json())

        #         assert isinstance(response.json(), dict)p
        #         assert isinstance(response.json()["channels"], list)

        pass

    @pytest.mark.parametrize("id_user,id_categ_1", [(3, "Sport")])
    def test_channels_by_categ_1(self, id_user, id_categ_1):
        """ """

        response = client.get(f"{prefix}/by_categ_1", params={"id_user": id_user})
        assert response.status_code == 200
        # assert response.json() == {"message": "Hello World"}

        logging.info(pformat(response.json()))
        assert isinstance(response.json(), dict)

        # select one categ_1
        sports = response.json()["id_categ_1"].get(id_categ_1, {})
        assert isinstance(sports, list)

        logging.info(pformat(sports))
        assert isinstance(sports[0], dict)

        # assert isinstance(response.json()["channels"], list)
