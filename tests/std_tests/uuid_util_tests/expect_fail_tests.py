from __future__ import annotations

from uuid import UUID

from red_utils.std import uuid_utils

from pytest import mark, xfail

@mark.xfail
def test_fail_gen_uuid():
    assert isinstance(
        uuid_utils.gen_uuid(), str
    ), "Output of gen_uuid() must not be of type str for this test"


@mark.xfail
def test_fail_trim_uuid():
    assert (
        uuid_utils.trim_uuid(trim="one", in_uuid="This is a test") is not None
    ), "Failed assertion expected"


@mark.xfail
def test_fail_first_n_chars():
    assert (
        uuid_utils.first_n_chars(first_n=15, in_uuid=None) is None
    ), "Failed assertion expected"


@mark.xfail
def test_fail_get_rand_uuid():
    rand_uuid = uuid_utils.get_rand_uuid()

    assert not isinstance(rand_uuid, str), "Failed assertion expected"
    assert rand_uuid is None, "Failed assertion expected"


@mark.xfail
def test_fail_trim_uuid(_uuid: UUID):
    assert isinstance(_uuid, str), f"_uuid must be of type str, not ({type(_uuid)})"
    fail_uuid = None
    trimmed = uuid_utils.trim_uuid(in_uuid=fail_uuid)
    assert trimmed is not None, "trimmed UUID cannot be None"


@mark.xfail
def test_fail_first_n_chars(_uuid: UUID):
    first_n = 15
    new_str = uuid_utils.first_n_chars(first_n=first_n, in_uuid=_uuid)

    assert len(new_str) == 16, "Failed assertion expected"
