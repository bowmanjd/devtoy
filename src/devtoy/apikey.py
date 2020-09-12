"""Manage dev.to API key."""

import contextlib
import getpass
import pathlib
import tempfile

KEY_DIR = pathlib.Path(tempfile.gettempdir(), "devtoy")
KEY_FILE = KEY_DIR / "apikey.txt"


def destroy() -> None:
    """Zero fill and delete API key file."""
    with contextlib.suppress(FileNotFoundError):
        with KEY_FILE.open("wb") as handle:
            handle.seek(50)
            handle.write(b"\0")
        KEY_FILE.unlink(True)


def obtain() -> str:
    """Get API key from file or prompt.

    Returns:
        API key
    """
    try:
        api_key = read()
    except FileNotFoundError:
        api_key = prompt()
        write(api_key)
    return api_key


def prompt() -> str:
    """Credential entry helper.

    Returns:
        credentials
    """
    api_key = getpass.getpass("dev.to API key: ")
    return api_key


def read() -> str:
    """Get API key.

    Returns:
        API key
    """
    return KEY_FILE.read_text()


def write(api_key: str) -> None:
    """Create/update API key file with API key.

    Args:
        api_key: the API key to be recorded
    """
    KEY_DIR.mkdir(exist_ok=True)
    KEY_FILE.write_text(api_key)
