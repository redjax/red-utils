from __future__ import annotations

from red_utils.std import dict_utils

from pytest import fixture

@fixture
def bad_dict() -> dict:
    _dict = ("test", "bad", "dict")

    return _dict


@fixture
def good_dict() -> dict:
    _dict = {"test": "value", "test2": 1}

    return _dict


@fixture
def merge_dict1() -> dict:
    _dict = {"name": "Example", "age": 21, "gender": "male"}

    return _dict


@fixture
def merge_dict2() -> dict:
    _dict = {"name": "Example2", "age": 50, "gender": "female"}

    return _dict


@fixture
def update_dict_original_dict() -> dict:
    _dict = {"var1": "val1", "var2": "val2", "var3": 15, "var4": False}

    return _dict


@fixture
def debug_dict_obj() -> dict:
    _dict = {
        "name": "Jeffrey",
        "age": 25,
        "gender": "male",
        "inventory": ["hammer", "screwdriver", "juicebox"],
    }

    return _dict
