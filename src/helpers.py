from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta
from secrets import token_hex


def verify_token(token: str):
    """verify token"""

    params = dotenv_values(".env")
    if token == params.get("TOKEN", None):
        return True
    return False


def make_now():
    """return current date and time"""

    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def make_time_delta(days: int):
    """return yesterday date and time"""

    past = datetime.now() - timedelta(days=days)
    return past.strftime("%Y-%m-%d %H:%M:%S")


def make_token(n=4, test=True):
    """return a token"""

    token = token_hex(n)
    token = token if not test else "test_" + token

    return token


def fake_token(n=6):
    """return a token"""

    token = token_hex(n)
    # token = token if not test else "test_" + token

    return "fake_" + token
