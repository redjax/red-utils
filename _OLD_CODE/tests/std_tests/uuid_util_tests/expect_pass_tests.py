from __future__ import annotations

from uuid import UUID

from red_utils.std import uuid_utils

from pytest import mark, xfail


@mark.uuid_utils
def test_gen_uuid():
    _uuid = uuid_utils.gen_uuid()

    assert _uuid is not None, "_uuid cannot be None"
    assert isinstance(_uuid, UUID), f"_uuid must be of type UUID, not ({type(_uuid)})"


@mark.uuid_utils
def test_gen_uuid_str():
    _uuid = uuid_utils.gen_uuid(as_hex=True)

    assert _uuid is not None, "_uuid cannot be None"
    assert isinstance(_uuid, str), f"_uuid must be of type str, not ({type(_uuid)})"


@mark.uuid_utils
def test_trim_uuid(_uuid: UUID):
    assert _uuid is not None, "_uuid cannot be None"
    assert isinstance(_uuid, UUID) or isinstance(
        _uuid, str
    ), f"_uuid must be of type str or UUID, not ({type(_uuid)})"

    trimmed = uuid_utils.trim_uuid(trim=12, in_uuid=_uuid)
    assert trimmed is not None, "trimmed UUID cannot be None"
    assert isinstance(trimmed, str), "trimmed should be of type str"

    orig_len = len(str(_uuid))
    new_len = len(trimmed)

    assert new_len == (
        orig_len - 12
    ), "trimmed UUID should be 12 characters less than original _uuid"


@mark.uuid_utils
def test_trim_uuid_str(_uuid_str: str):
    assert _uuid_str is not None, "_uuid_str cannot be None"
    assert isinstance(
        _uuid_str, str
    ), f"_uuid_str must be of type str, not ({type(_uuid_str)})"

    trimmed = uuid_utils.trim_uuid(trim=12, in_uuid=_uuid_str)
    assert trimmed is not None, "trimmed UUID cannot be None"
    assert isinstance(trimmed, str), "trimmed should be of type str"

    orig_len = len(str(_uuid_str))
    new_len = len(trimmed)

    assert new_len == (
        orig_len - 12
    ), "trimmed UUID should be 12 characters less than original _uuid"


@mark.uuid_utils
def test_first_n_chars(_uuid: UUID):
    first_n = 15
    new_str = uuid_utils.first_n_chars(first_n=first_n, in_uuid=_uuid)

    assert len(new_str) == first_n, f"Length of new_str should be {first_n}"


@mark.uuid_utils
def test_get_rand_uuid():
    _uuid = uuid_utils.get_rand_uuid(as_str=False)

    assert _uuid is not None, "_uuid must not be None"
    assert isinstance(_uuid, UUID), f"_uuid must be of type UUID, not ({type(_uuid)})"
    assert len(str(_uuid)) == 36, f"_uuid length should be 36, not {len(_uuid)}"


@mark.uuid_utils
def test_get_rand_uuid_trim():
    trim = 15
    _uuid = uuid_utils.get_rand_uuid(trim=trim)

    assert _uuid is not None, "_uuid must not be None"
    assert isinstance(_uuid, str), "_uuid must be of type str"
    assert (
        len(_uuid) == 36 - trim
    ), f"_uuid length must be {36 - trim}, not {len(_uuid)}"


@mark.uuid_utils
def test_get_rand_uuid_str(_uuid_str: str):
    assert _uuid_str is not None, "_uuid_str must not be None"
    assert isinstance(_uuid_str, str), "_uuid_str must be of type str"
