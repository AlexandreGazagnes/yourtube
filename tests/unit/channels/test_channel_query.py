import logging

# Import TestClient and your FastAPI app
# from fastapi.testclient import TestClient
# from src import app
import pytest


from src.channels.queries import ChannelQuery
from src.channels.queries import _query_channel_by_id


class TestChannelQuery:
    """TestChannelQueries"""

    @pytest.mark.parametrize("id_channel", [("UC-06IzcwOHu9_Xgqr-NMkUQ",)])
    def test_channel_by_id(self, id_channel):
        """test simple query"""

        results = _query_channel_by_id(id_channel)

        assert isinstance(results, dict)

        logging.info(results)
