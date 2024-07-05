from __future__ import annotations

from pytest import mark, xfail
from red_utils.std import dict_utils


@mark.dict_utils
def test_valid_dict(good_dict: dict):
    assert good_dict is not None, "Example good_dict cannot be None"
    assert isinstance(
        good_dict, dict
    ), f"good_dict must be of type dict, not ({type(good_dict)})"


@mark.dict_utils
def test_merge_dicts(merge_dict1: dict, merge_dict2: dict):
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


@mark.dict_utils
def test_update_dict(
    update_dict_original_dict: dict, update_vals: dict = {"var4": True}
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


@mark.dict_utils
def test_debug_dict(debug_dict_obj: dict):
    assert debug_dict_obj is not None, "debug_dict_obj cannot be None"
    assert isinstance(
        debug_dict_obj, dict
    ), f"debug_dict_obj must be of type dict, not ({type(debug_dict_obj)})"
    dict_utils.debug_dict(in_dict=debug_dict_obj)
