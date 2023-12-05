from dotenv import load_dotenv, dotenv_values
from datetime import datetime, timedelta
from secrets import token_hex


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


def stringify_duration(duration: int):
    """return a stringified duration"""

    duration = int(duration)
    mins = int(duration // 60)
    secs = int(duration % 60)

    if mins < 60:
        return f"{mins}:{secs}"

    hours = int(mins // 60)
    mins = int(mins % 60)

    return f"{hours}:{mins}:{secs}"


def sringify_publihed_at(date: str):
    """return a stringified date"""

    # date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    # return date.strftime("%d %B %Y")

    pass


def translate_front_publised_at(text: str) -> int:
    """return a translated date"""

    # date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    # return date.strftime("%d %B %Y")

    if not text:
        return None
    if text.strip() == "-":
        return None

    if "day" in text:
        return 1
    if "week" in text:
        return 7
    if "month" in text:
        return 30
    if "year" in text:
        return 365
    return 36_500


def translate_front_duration(text: str) -> int:
    """ """

    if not text:
        return None

    if text.strip() == "-":
        return None

    nb, unit = text.split(" ")
    nb = int(nb)

    factor = 0

    if "min" in unit:
        factor = 60
    if "hour" in unit:
        factor = 3600

    seconds = nb * factor

    return seconds
