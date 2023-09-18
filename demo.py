import pkgutil

## stdlib utils
from red_utils.utils import file_utils, context_managers, dict_utils, hash_utils, uuid_utils, time_utils

if pkgutil.find_loader("msgpack"):
    from red_utils.utils import msgpack_utils
if pkgutil.find_loader("diskcache"):
    from red_utils.utils import diskcache_utils
if pkgutil.find_loader("httpx"):
    from red_utils.utils import httpx_utils
if pkgutil.find_loader("fastapi"):
    from red_utils.utils import fastapi_utils
    
    if pkgutil.find_loader("uvicorn"):
        import uvicorn
if pkgutil.find_loader("sqlalchemy"):
    from red_utils.utils import sqlalchemy_utils


from red_utils import CustomException
import random
from pathlib import Path

from time import sleep
import uuid
from typing import Union

import json



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


def test_msgpack_utils() -> dict[str, msgpack_utils.SerialFunctionResponse]:
    msgpack_utils.ensure_path(".serialize")

    test_dict: dict = {
        "test": 1,
        "test2": 2,
        "test3": {"test4": 4, "test5": 5},
        "test6": ["test7", "test8"],
        "test9": [
            {"test10": 10, "test11": 11},
            {"test12": 12, "test13": ["test14", "test15"]},
        ],
    }

    test_json: str = json.dumps(test_dict)

    def _serialize(string: str = test_json) -> msgpack_utils.SerialFunctionResponse:
        _serial: msgpack_utils.SerialFunctionResponse = msgpack_utils.msgpack_serialize(
            _json=string
        )

        return _serial

    def _deserialize(string: bytes = None):
        _deserial: str = msgpack_utils.msgpack_deserialize(packed_str=string)

        return _deserial

    def _serialize_file(
        string: str = test_json, file: str = ".serialize/test_serialize.msgpack"
    ):
        file_path = Path(file)
        file_dir = file_path.parent
        file_name = file_path.name

        _serial = msgpack_utils.msgpack_serialize_file(
            _json=string, output_dir=file_dir, filename=file_name
        )

        return _serial

    def _deserialize_file(file: str = None):
        _deserial = msgpack_utils.msgpack_deserialize_file(filename=file)

        return _deserial

    serial_str = _serialize()
    # print(f"Serialized ({type(serial_str)}): {serial_str}")
    deserial_str = _deserialize(string=serial_str.detail)
    # print(f"Deserialized ({type(deserial_str)}): {deserial_str}")

    serial_file = _serialize_file()
    # print(f"Serialize to file ({type(serial_file)}): {serial_file}")
    deserial_file = _deserialize_file(file=serial_file.detail)
    # print(f"Deserialize from file ({type(deserial_file)}): {deserial_file}")

    return_obj = {
        "serialized_string": serial_str,
        "deserialized_str": deserial_str,
        "serialized_file": serial_file,
        "deserialized_file": deserial_file,
    }

    return return_obj


def test_diskcache_utils():
    test_cache = diskcache_utils.new_cache(
        cache_conf=diskcache_utils.default_cache_conf
    )

    diskcache_utils.set_val(cache=test_cache, key=1, val="test")
    read_val = diskcache_utils.get_val(cache=test_cache, key=1)
    # print(f"Read val ({type(read_val)}): {read_val}")

    cache_check: list = diskcache_utils.check_cache(cache=test_cache)

    key_exists: bool = diskcache_utils.check_cache_key_exists(cache=test_cache, key=1)

    cache_size: dict = diskcache_utils.get_cache_size(cache=test_cache)

    convert_2m_to_s = diskcache_utils.convert_to_seconds(amount=2, unit="minutes")

    _del: str = diskcache_utils.delete_val(cache=test_cache, key=1)

    init_cache_check_after_del = diskcache_utils.check_cache_key_exists(
        cache=test_cache, key=1
    )

    create_after_del = diskcache_utils.set_val(
        cache=test_cache, key=1, val="test_after_delete"
    )

    check_after_del_recreate: bool = diskcache_utils.check_cache_key_exists(
        cache=test_cache, key=1
    )

    clear_cache: bool = diskcache_utils.clear_cache(cache=test_cache)

    check_after_clear: bool = diskcache_utils.check_cache_key_exists(
        cache=test_cache, key=1
    )

    create_after_clear = diskcache_utils.set_val(
        cache=test_cache, key=1, val="test_after_clear"
    )
    cache_check_after_clear = diskcache_utils.check_cache_key_exists(
        cache=test_cache, key=1
    )

    return_obj = {
        "cache": test_cache,
        "cache_check": cache_check,
        "initial_read": read_val,
        "initial_exist": key_exists,
        "initial_cache_size": cache_size,
        "converted_2m_to_2s": convert_2m_to_s,
        "del_1": _del,
        "check_after_del_1": init_cache_check_after_del,
        "check_after_del_2": check_after_del_recreate,
        "create_after_del": create_after_del,
        "clear_cache": clear_cache,
        "check_after_clear_1": check_after_clear,
        "create_after_clear": create_after_clear,
        "check_after_clear_2": cache_check_after_clear,
    }

    return return_obj


def test_httpx_utils():
    default_headers = httpx_utils.default_headers

    test_client = httpx_utils.get_req_client(headers=default_headers)

    res = httpx_utils.make_request(
        client=test_client, url="https://pokeapi.co/api/v2/pokemon/gengar"
    )

    return_obj = {"status_code": res.status_code, "reason": res.reason_phrase}

    return return_obj


def test_fastapi_utils():
    app = fastapi_utils.get_app()
    print(f"App ({type(app)}): {app}")

    return app


def test_sqlalchemy_utils():
    base = sqlalchemy_utils.Base()
    connection = sqlalchemy_utils.saSQLiteConnection()
    print(f"Connection: {connection}")
    engine = sqlalchemy_utils.get_engine(connection=connection, echo=True)
    SessionLocal = sqlalchemy_utils.get_session(engine=engine)
    sqlalchemy_utils.create_base_metadata(base_obj=base, engine=engine)


def main():
    """Main function to control flow of demo.

    Comment functions you don't want to execute.
    """
    # print(test_file_utils_list())

    # test_context_managers()

    # test_dict_utils()

    # test_hash_utils()

    # test_uuid_utils()

    # test_time_utils()

    # print(test_msgpack_utils())

    # print(test_diskcache_utils())

    # print(test_httpx_utils())

    # fastapi_app = test_fastapi_utils()
    # uvicorn.run(fastapi_app)

    test_sqlalchemy_utils()


if __name__ == "__main__":
    main()
