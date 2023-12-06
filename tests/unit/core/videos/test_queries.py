import logging

import pytest

from src.core.videos.queries import CoreVideoQueries
from src.db import Session, engine

from src.params import get_params, params
from src.db import Db

# verbose = True


class TestQueries:
    """Test queries"""

    def test_query_one(self, verbose: bool = True):
        """test query_one"""

        id_video = "69cq3gWQKgU"
        id_channel = "UCOjD18EJYcsBog4IozkF_7w"

        results = CoreVideoQueries.query_one(id_channel, engine=None)

        assert isinstance(results, dict)
        assert results

        logging.warning(f"results: {results}")
