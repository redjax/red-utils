"""Tests designed to fail when run with pytest."""

from __future__ import annotations

from red_utils.std import dict_utils

from pytest import mark, xfail

@mark.xfail
def test_fail_debug_dict_none(_dict: dict = None):
    assert _dict is not None, "_dict cannot be None"
    assert isinstance(_dict, dict), f"_dict must be of type dict, not ({type(_dict)})"


@mark.xfail
def test_fail_debug_dict(bad_dict: dict = None):
    dict_utils.debug_dict(in_dict=bad_dict)


@mark.xfail
def test_fail_merge_dicts(merge_dict1: dict, merge_dict2: dict = None):
    assert merge_dict1 is not None, "merge_dict1 cannot be None"
    assert isinstance(
        merge_dict1, dict
    ), f"merge_dict1 must be of type dict, not ({type(merge_dict1)})"

    assert merge_dict2 is not None, "merge_dict2 cannot be None"
    assert isinstance(
        merge_dict2, dict
    ), f"merge_dict2 must be of type dict, not ({type(merge_dict2)})"

    merged = dict_utils.merge_dicts(original_dict=merge_dict1, update_vals=merge_dict2)
    assert merged is not None, "Merging dicts failed"
    assert isinstance(
        merged, dict
    ), f"merged must be of type dict, not ({type(merged)})"


@mark.xfail
def test_fail_update_dict(
    update_dict_original_dict: dict, update_vals: dict = [1, True]
):
    assert (
        update_dict_original_dict is not None
    ), "update_dict_original_dict cannot be None"
    assert isinstance(
        update_dict_original_dict, dict
    ), f"update_dict_original_dict must be of type dict, not ({type(update_dict_original_dict)})"

    assert update_vals is not None, "update_vals cannot be None"
    assert isinstance(
        update_vals, dict
    ), f"update_vals must be of type dict, not ({type(update_vals)})"
