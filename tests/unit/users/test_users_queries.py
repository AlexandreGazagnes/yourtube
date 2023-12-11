import logging, json

from src.users.queries import (
    _pre_query_channels,
    _pre_query_preferences,
    _pre_query_last_videos,
    _query_user_counts,
    _query_preferences,
)


class TestUnitUserQuery:
    """test user queries"""

    def test_counts(self, verbose: bool = True, csv: bool = True):
        """test counts"""

        payload = _query_user_counts()

        # assert isinstance(payload, dict)
        # assert "users" in payload.keys()
        # assert isinstance(payload["users"], int)

        if verbose:
            logging.info(payload)

    def test_pre_query_preferences(self, verbose: bool = True, csv: bool = True):
        """test preferences"""

        payload = _pre_query_preferences(id_user=3)

        # assert isinstance(payload, dict)
        # assert "id_user" in payload.keys()
        # assert isinstance(payload["id_user"], int)

        if verbose:
            logging.info(payload)

    def test_pre_query_channels(self, verbose: bool = True, csv: bool = True):
        """test channels"""

        id_channel_list = ["UCa3riqqrEl0I57LJEGbEM4Q", "UCENv8pH4LkzvuSV_qHIcslg"]
        payload = _pre_query_channels(id_channel_list=id_channel_list)

        # assert isinstance(payload, list)
        # assert isinstance(payload[0], dict)
        # assert "id_channel" in payload[0].keys()
        # assert isinstance(payload[0]["id_channel"], int)

        if verbose:
            logging.info(payload)

    def test_pre_query_last_videos(self, verbose: bool = True, csv: bool = True):
        """test last videos"""

        id_channel = "UCENv8pH4LkzvuSV_qHIcslg"
        payload = _pre_query_last_videos(id_channel)

        # assert isinstance(payload, list)
        # assert isinstance(payload[0], dict)

        if verbose:
            logging.info(payload)

    def test_query_preferences(self, verbose: bool = True, csv: bool = True):
        """test preferences"""

        payload = _query_preferences(id_user=3)

        # assert isinstance(payload, dict)
        # assert "id_user" in payload.keys()
        # assert isinstance(payload["id_user"], int)

        # if verbose:
        #     logging.info(payload)

        if csv:
            txt = json.dumps(payload, indent=4)
            with open("tmp/test_users_queries.json", "w") as f:
                f.write(txt)
