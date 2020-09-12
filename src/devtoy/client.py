"""Interact with dev.to API."""

import asyncio
import json
import pathlib

import httpx
import typer

from devtoy import apikey

BASE_URL = "https://dev.to/api"
APP = typer.Typer()


async def request(
    path: str,
    params: dict = None,
    method: str = "get",
    connection: httpx.AsyncClient = None,
) -> httpx.Response:
    """Process HTTP request.

    Args:
        path: endpoint for call
        params: parameters dict
        method: get or post
        connection: optional async client

    Returns:
        response body
    """
    if connection:
        close_client = False
    else:
        connection = httpx.AsyncClient()
        close_client = True

    url = BASE_URL + path
    response = await connection.request(
        method, url, params=params, headers={"api-key": apikey.obtain()}
    )
    if close_client:
        await connection.aclose()
    return response


async def save_article(filename: str, markdown: str) -> None:
    """Pass the markdown content to prettier and save.

    Args:
        filename: path to file
        markdown: markdown content
    """
    command = f"prettier --parser markdown > {filename}"
    process = await asyncio.create_subprocess_shell(
        command, stdin=asyncio.subprocess.PIPE
    )
    await process.communicate(markdown.encode())


async def download_articles(directory: pathlib.Path) -> None:
    """Download articles.

    Args:
        directory: path to directory in which to download files
    """
    response = await request("/articles/me/published")
    saves = [
        save_article(str(directory / f"{post['slug']}.md"), post["body_markdown"])
        for post in response.json()
    ]
    await asyncio.gather(*saves)


@APP.command()
def articles() -> None:
    """List articles."""
    response = asyncio.run(request("/articles/me/published"))
    print(json.dumps(response.json(), indent=2))


@APP.command()
def save(directory: str = ".") -> None:
    """Download articles.

    Args:
        directory: path to directory in which to download files
    """
    location = pathlib.Path(directory).resolve()
    location.mkdir(exist_ok=True)
    asyncio.run(download_articles(location))


def cli() -> None:
    """Run commands."""
    APP()
