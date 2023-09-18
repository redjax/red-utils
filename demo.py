from red_utils.utils import (
    file_utils,
    context_managers,
    dict_utils,
    hash_utils,
    uuid_utils,
    time_utils,
)
from red_utils import CustomException
import random
from pathlib import Path

from time import sleep
import uuid
from typing import Union


def test_file_utils_list() -> list[Path]:
    cwd = Path.cwd()
    search_dir = f"{cwd}/red_utils"

    list_files_test = file_utils.list_files(in_dir=search_dir, ext_filter=".py")
    print(f".py files found in {search_dir}: {len(list_files_test)}")

    rand_index = random.randint(0, len(list_files_test) - 1)
    print(f"Example util file: {list_files_test[rand_index]}")

    file_dicts: list[dict] = []

    try:
        for f in list_files_test:
            f_dict: dict = {"name": None, "path": None}

            f_dict["name"] = f.name
            f_dict["path"] = f.parent

            file_dicts.append(f_dict)

        return file_dicts

    except Exception as exc:
        raise CustomException(
            "Unhandled exception creating dict.",
            errors=exc,
            extra={"Exception type": exc.__class__},
        )


def test_context_managers(limit: int = 5, _sleep: int = 1) -> None:
    def benchmark_test(limit=limit, _sleep=_sleep) -> None:
        with context_managers.benchmark("Test benchmark"):
            current_count: int = 0

            while current_count < limit:
                print(f"Count: {current_count}")
                current_count += 1

                sleep(_sleep)

    def protected_list_test(
        original_list: list[str] = ["item1", "item2", "item3"]
    ) -> list[str]:
        print(f"List before protected update: {original_list}")

        with context_managers.ListProtect(original=original_list) as copy:
            copy.append("item4")

        return original_list

    def protected_dict_test(
        original_dict: dict[str, int] = {"one": 1, "two": 2, "three": 3}
    ) -> dict[str, int]:
        print(f"Dict before protected update: {original_dict}")

        with context_managers.DictProtect(original=original_dict) as copy:
            copy["four"] = 4

        return original_dict

    def sqlite_manager_test(db_path: str = "test.db"):
        with context_managers.SQLiteConnManager(path=db_path) as db:
            db.get_tables()

    benchmark_test()

    print(f"List after protected copy: {protected_list_test()}")

    print(f"Dict after protected copy: {protected_dict_test()}")

    sqlite_manager_test()


def test_dict_utils():
    def _debug(
        test_dict: dict = {
            "test": 1,
            "test2": {"test3": 3},
            "test4": ["test5", "test6"],
        }
    ):
        dict_utils.debug_dict(in_dict=test_dict)

    def _merge(
        original: dict = {"one": 1, "two": 2}, update: dict = {"three": 3}
    ) -> dict:
        print(f"Original dict: {original}")
        print(f"Update values: {update}")
        _merged: dict = dict_utils.merge_dicts(original, update)

        return _merged

    def _update(original: dict = {"one": 1, "two": 2}, update: dict = {"three": 3}):
        print(f"Original dict: {original}")
        print(f"Update values: {update}")
        _updated: dict = dict_utils.update_dict(original, update)

        return _updated

    def _validate(in_dict: dict = {"test": 1}) -> dict:
        _valid: dict = dict_utils.validate_dict(_dict=in_dict)

        return _valid

    _debug()
    print(f"Merged dicts: {_merge()}")
    print(f"Updated dict: {_update()}")
    print(f"Validated dict: {_validate()}")


def test_hash_utils(string: str = "This is a test string") -> str:
    _hash: str = hash_utils.get_hash_from_str(input_str=string)
    print(f"String: {string}\nHash: {_hash}")

    return _hash


def test_uuid_utils():
    def _first_n(in_uuid: uuid.UUID = uuid.uuid4(), first_n: int = 10) -> dict:
        print(f"Trimming UUID: {in_uuid} to first {first_n} characters")
        non_hex: str = uuid_utils.first_n_chars(in_uuid=in_uuid, first_n=first_n)
        _hex: str = uuid_utils.first_n_chars(
            in_uuid=in_uuid, first_n=first_n, as_hex=True
        )

        return {"non-hex": non_hex, "hex": _hex}

    def _gen():
        non_hex: Union[str, uuid.UUID] = uuid_utils.gen_uuid()
        _hex: Union[str, uuid.UUID] = uuid_utils.gen_uuid(as_hex=True)

        return {"non-hex": non_hex, "hex": _hex}

    def _rand():
        _rand: Union[str, uuid.UUID] = uuid_utils.get_rand_uuid()
        _trim: Union[str, uuid.UUID] = uuid_utils.get_rand_uuid(trim=5)
        _chars: Union[str, uuid.UUID] = uuid_utils.get_rand_uuid(characters=5)
        _hex = uuid_utils.get_rand_uuid(as_hex=True)

        return {
            "random": _rand,
            "random_trimmed": _trim,
            "random_5_chars": _chars,
            "random_hex": _hex,
        }

    def _trim(in_uuid=uuid_utils.get_rand_uuid(), trim=12):
        _trimmed = uuid_utils.trim_uuid(in_uuid=in_uuid, trim=trim)
        _trimmed_hex = uuid_utils.trim_uuid(in_uuid=in_uuid, trim=trim, as_hex=True)

        return {"non-hex": _trimmed, "hex": _trimmed_hex}

    print(_first_n())
    print(_gen())
    print(_rand())
    print(_trim())


def test_time_utils():
    fmt: str = time_utils.default_format
    fmt_12: str = time_utils.twelve_hour_format

    def dt_as_dt(ts=time_utils.get_ts(), fmt=fmt):
        _dt = time_utils.datetime_as_dt(ts=ts, format=fmt)

        return _dt

    def dt_as_str(ts=time_utils.get_ts(), fmt=fmt):
        _dt = time_utils.datetime_as_str(ts=ts, format=fmt)

        return _dt

    now_unformatted = time_utils.get_ts(format=fmt)
    now = now_unformatted.strftime(time_utils.default_format)
    print(f"Timestamp ({type(now_unformatted)}): {now_unformatted}")
    print(f"Timestamp formatted ({type(now)}): {now}")

    # now_default_dt = dt_as_dt(ts=now)
    # now_default_dt_12h = dt_as_dt(ts=now, fmt=fmt_12)
    # now_default_str = dt_as_str(ts=now)
    # now_default_str_12h = dt_as_str(ts=now, fmt=fmt_12)

    return {
        "now_unformatted": now_unformatted,
        "now": now,
        # "now_dt": now_default_dt,
        # "now_str": now_default_str,
        # "now_dt_12h": now_default_dt_12h,
        # "now_str_12h": now_default_str_12h,
    }


def main():
    """Main function to control flow of demo.

    Comment functions you don't want to execute.
    """
    # print(test_file_utils_list())

    # test_context_managers()

    # test_dict_utils()

    # test_hash_utils()

    # test_uuid_utils()

    test_time_utils()


if __name__ == "__main__":
    main()
