from __future__ import annotations

import pytest

from red_utils.std import hash_utils


@pytest.fixture
def str_to_hash() -> str:
    hash_str = "This is a string that will be used for hash_utils tests."

    return hash_str


@pytest.fixture
def hashed_str() -> str:
    _hashed = hash_utils.get_hash_from_str(input_str=str_to_hash())

    return _hashed
