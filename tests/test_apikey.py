"""Test apikey submodule."""
import getpass

from devtoy import apikey

API_KEY = "abcdefghij"


def fake_getpass(prompt: str) -> str:  # noqa:SC100,W0613
    """Mock getpass."""
    return API_KEY


def test_obtain_fresh(monkeypatch):
    """Test obtaining the API key when not cached."""
    monkeypatch.setattr(getpass, "getpass", fake_getpass)
    apikey.destroy()
    key = apikey.obtain()
    assert key == API_KEY


def test_obtain_cached():
    """Test obtaining the API key when already cached."""
    apikey.write(API_KEY)
    key = apikey.obtain()
    assert key == API_KEY
