import logging

# Import TestClient and your FastAPI app
# from fastapi.testclient import TestClient
# from src import app
import pytest


from src.channels.queries import ChannelQuery
from src.channels.queries import _query_channel_by_id, _query_channels_by_user


class TestChannelsQueries:
    """TestChannelsQueries"""

    @pytest.mark.parametrize("id_user", [3])
    def test_channels_by_user(self, id_user):
        """test simple query"""

        results = _query_channels_by_user(id_user)

        logging.info(results)

        assert isinstance(results, list)
        assert isinstance(results[0], dict)
