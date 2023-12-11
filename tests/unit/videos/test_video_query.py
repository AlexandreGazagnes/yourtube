import logging

import pytest

from src.videos.queries import _query_video_by_id


class TestUnitVideoQuery:
    """TestVideoQuery"""

    @pytest.mark.parametrize("id_video", [("_URmd_ff8HU",)])
    def test_channel_by_id(self, id_video):
        """test simple query"""

        results = _query_video_by_id(id_video)

        assert isinstance(results, dict)

        logging.info(results)
