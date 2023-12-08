import logging, json

from src.videos.queries import (
    _query_video_count,
    _query_all_id_videos,
    _query_video_by_user,
    _query_video_by_channel,
)


class TestVideosQuery:
    """test user queries"""

    def test_query_video_count(self, verbose: bool = True, csv: bool = True):
        """test counts"""

        payload = _query_video_count()

        # assert isinstance(payload, dict)
        # assert "users" in payload.keys()
        # assert isinstance(payload["users"], int)

        if verbose:
            logging.info(payload)

    def test_query_all_id_videos(self, verbose: bool = True, csv: bool = True):
        """test preferences"""

        payload = _query_all_id_videos()

        # assert isinstance(payload, dict)
        # assert "id_user" in payload.keys()
        # assert isinstance(payload["id_user"], int)

        payload = payload[:10]

        if verbose:
            logging.info(payload)

    def test_query_video_by_user(self, verbose: bool = True, csv: bool = True):
        """test channels"""

        id_user = 3
        result, _ = _query_video_by_user(id_user=id_user)

        # assert isinstance(payload, list)
        # assert isinstance(payload[0], dict)
        # assert "id_channel" in payload[0].keys()
        # assert isinstance(payload[0]["id_channel"], int)

        result = result[:10]
        if verbose:
            logging.info(result)

    def test_query_video_by_channel(self, verbose: bool = True, csv: bool = True):
        """ """

        # cest pas sorcier
        id_channel = "UCENv8pH4LkzvuSV_qHIcslg"

        result, _ = _query_video_by_channel(id_channel=id_channel, days_max=360)

        result = result[:10]
        if verbose:
            logging.info(result)
