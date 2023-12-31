from __future__ import annotations

from dataclasses import dataclass, field
from typing import Union

from red_utils.core.dataclass_utils import DictMixin
from red_utils.validators.ext.httpx_validators import (
    valid_methods,
    validate_client,
    validate_headers,
    validate_method,
)

from .constants import default_headers

import httpx

@dataclass
class SimpleHTTPXClientBase:
    method: str | None = field(default="GET")
    headers: dict | None = field(default=default_headers)
    timeout: int | None = field(default=5)
    data: Union[dict, str] | None = field(default=None)

    def __post_init__(self):
        self.method = self.method.upper()
        validate_method(self.method)
        validate_headers(self.headers)

    def client(self) -> httpx.Client:
        try:
            _client = httpx.Client(headers=self.headers, timeout=self.timeout)

            return _client
        except Exception as exc:
            raise Exception(f"Unhandled exception getting HTTPX Client. Details: {exc}")


@dataclass
class SimpleHTTPXClient(SimpleHTTPXClientBase):
    pass
