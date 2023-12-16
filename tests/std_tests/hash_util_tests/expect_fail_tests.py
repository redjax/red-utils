from __future__ import annotations

from red_utils.std import hash_utils

from pytest import mark, xfail

@mark.xfail
def test_fail_str_to_hash(str_to_hash: str = None):
    assert str_to_hash is not None, "str_to_hash cannot be None"
    assert isinstance(
        str_to_hash, str
    ), f"str_to_hash must be of type str, not ({type(str_to_hash)})"


@mark.xfail
def test_fail_hash_a_str(str_to_hash: str = None):
    assert (
        hash_utils.get_hash_from_str(input_str=str_to_hash) is not None
    ), "Output hashed string cannot be None"
