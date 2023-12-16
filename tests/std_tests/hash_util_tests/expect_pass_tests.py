from __future__ import annotations

from red_utils.std import hash_utils

from pytest import mark, xfail

@mark.hash_utils
def test_validate_hash_str(str_to_hash: str):
    assert str_to_hash is not None, "str_to_hash cannot be None"
    assert isinstance(
        str_to_hash, str
    ), f"str_to_hash must be of type str, not ({type(str_to_hash)})"


@mark.hash_utils
def test_hash_str(str_to_hash: str):
    hashed = hash_utils.get_hash_from_str(input_str=str_to_hash)
    assert hashed is not None, "Hashed string cannot be None"
    assert isinstance(
        hashed, str
    ), f"Hashed string must be of type str, not ({type(hashed)})"
