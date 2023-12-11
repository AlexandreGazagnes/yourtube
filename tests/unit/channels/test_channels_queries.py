import logging
from pprint import pprint, pformat

# Import TestClient and your FastAPI app
# from fastapi.testclient import TestClient
# from src import app
import pytest


from src.channels.queries import ChannelQuery
from src.channels.queries import _query_channels_by_user, _query_channels_by_categ_1


class TestUnitChannelsQueries:
    """TestChannelsQueries"""

    @pytest.mark.parametrize("id_user", [3])
    def test_channels_by_user(self, id_user):
        """test simple query"""

        results, _ = _query_channels_by_user(id_user)

        logging.info(results)

        assert isinstance(results, list)
        assert isinstance(results[0], dict)

    @pytest.mark.parametrize("id_user", [(3)])
    def test_channels_by_categ_1(self, id_user):
        """test simple query"""

        results, _ = _query_channels_by_categ_1(id_user)

        logging.info(pformat(results))

        assert isinstance(results, dict)
        assert isinstance(results[0], list)
        assert isinstance(results[0][0], dict)
