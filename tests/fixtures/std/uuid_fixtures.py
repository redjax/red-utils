from __future__ import annotations

from uuid import UUID

from pytest import fixture
from red_utils.std import uuid_utils

@fixture
def _uuid() -> UUID:
    _id = uuid_utils.gen_uuid()

    return _id


@fixture
def _uuid_str() -> str:
    _id = uuid_utils.gen_uuid(as_hex=True)

    return _id
