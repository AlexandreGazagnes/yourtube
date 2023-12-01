import pytest

from src.params import get_params


def test_get_params():
    """Test get_params function"""

    params = get_params(MODE="dev")
    assert params["host"] == "http://localhost"
    assert params["port"] == "8000"
    assert params["user"] == "root"
    assert params["password"] == "password"
    assert params["database"] == "yourdb"
    assert params["mode"] == "dev"
    assert params["api_token"] == "azerty"
    assert params["mysql_root_password"] == "password"
    assert params["mysql_database"] == "yourdb"
    assert params["mysql_password"] == "password"
    assert params["mysql_host"] == "http://localhost"
    assert params["mysql_port"] == "3306"
    assert params["pma_host"] == "db"
