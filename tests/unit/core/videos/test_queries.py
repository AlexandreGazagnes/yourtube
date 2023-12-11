import logging

import pytest

from src.params import get_params, params

from src.db import Session, engine
from src.db import Db

from src.core.videos.queries import _query_one

# verbose = True


class TestUnitQuery:
    """Test queries"""

    def test_query_one(self, verbose: bool = True):
        """test query_one"""

        # id_video = "69cq3gWQKgU"
        id_channel = "UCOjD18EJYcsBog4IozkF_7w"

        results = _query_one(id_channel, engine=None)

        assert isinstance(results, dict)
        assert results

        if verbose:
            logging.info(f"results: {results}")
