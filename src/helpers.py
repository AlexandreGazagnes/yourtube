from dotenv import load_dotenv, dotenv_values


def verify_token(token: str):
    """verify token"""

    params = dotenv_values(".env")
    if token == params.get("TOKEN", None):
        return True
    return False
