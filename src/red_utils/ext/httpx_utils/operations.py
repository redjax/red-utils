from __future__ import annotations

import typing as t
import logging

log = logging.getLogger("red_utils.ext.httpx_utils")

from .constants import (
    default_headers,
)
from .validators import (
    validate_client,
    validate_headers,
    validate_method,
)

import httpx
from httpx import Client


def merge_headers(
    original_headers: dict[str, str] = default_headers,
    update_vals: dict[str, str] = None,
) -> dict[str, str]:
    """Merge header dicts into new headers dict."""
    validate_headers(original_headers)
    validate_headers(update_vals)

    try:
        _headers: dict = {**update_vals, **original_headers}

    except Exception as exc:
        msg = Exception(f"Unhandled exception merging header dicts. Details: {exc}")
        log.error(msg)

        raise exc

    return _headers


def update_headers(
    original_headers: dict[str, str] = default_headers,
    update_vals: dict[str, str] = None,
) -> dict[str, str]:
    validate_headers(original_headers)
    validate_headers(update_vals)

    try:
        ## Create a copy of original_headers to update
        new_headers: dict[str, str] = original_headers.copy()
        ## Update new_headers with update_vals dict
        new_headers.update(update_vals)

        return new_headers

    except Exception as exc:
        msg = Exception(f"Unhandled exception updating headers. Details: {exc}")
        log.error(msg)

        raise exc


def get_req_client(
    headers: dict | None = default_headers, timeout: int | None = None
) -> httpx.Client:
    """Return a customized HTTPX client."""
    _client: Client = Client(headers=headers, timeout=timeout)

    validate_client(_client)

    return _client


def build_request(
    method: str = "GET",
    url: str = None,
    files: list | None = None,
    data: t.Any | None = None,
    content: bytes | None = None,
    params: dict | None = None,
    headers: dict | None = None,
    cookies: dict | None = None,
    stream: t.Union[httpx.SyncByteStream, httpx.AsyncByteStream] | None = None,
    extensions: dict | None = None,
) -> httpx.Request:
    """Build an `httpx.Request()` object from inputs.

    Params:
        method (str): (default="GET") The HTTP method for the request.
        url (str): The URL to send request to.
        files (list): List of files to send with request.
        data (Any): <UNDOCUMENTED>
        contents (bytes): Byte-encoded request content.
        params (dict): URL params for request. Pass each param as a key/value pair, like:
            `{"api_key": api_key, "days": 15, "page": 2}`
        headers (dict): Headers for request.
        cookies (dict): Cookies for request.
        extensions (dict): Extensions for request. Example: `{"timeout": {"connect": 5.0}}`.
        stream (httpx.SyncByteStream | httpx.AsyncByteSTream): <UNDOCUMENTED>
    """
    try:
        _request: httpx.Request = httpx.Request(
            method=method,
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            content=content,
            data=data,
            files=files,
            extensions=extensions,
            stream=stream,
        )
        return _request

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception building httpx.Request object. Details: {exc}"
        )
        log.error(msg)

        raise exc


def make_request(
    client: Client = None,
    url: str = None,
    method: str = "GET",
    headers: dict = None,
    timeout: int | None = None,
    data: dict | None = None,
) -> httpx.Response:
    """Make a request with HTTPX."""
    validate_method(method)

    if not client:
        log.warning(
            "No request client passed to make_request() function. Getting default client."
        )

        client = get_req_client(headers=headers, timeout=timeout)

    validate_client(client=client)

    if not isinstance(client, Client):
        raise TypeError(
            f"Invalid type for client: {type(client)}. Must be of type {type(Client)}"
        )

    if not url:
        raise ValueError("Missing request URL")

    if not isinstance(url, str):
        raise TypeError(f"Invalid type for request URL: {type(url)}")

    if timeout:
        if not isinstance(timeout, int):
            raise TypeError(f"Invalid type for timeout: {type(timeout)}")

    try:
        ## Determine type of request to make
        match method:
            case "GET":
                client = get_req_client(headers=headers, timeout=timeout)

                res = client.get(url=url)

            case _:
                raise ValueError(f"Invalid method: {method}")

        return res

    except Exception as exc:
        msg = Exception(f"Unhandled exception creating request client. Details: {exc}")
        log.error(msg)

        raise exc
