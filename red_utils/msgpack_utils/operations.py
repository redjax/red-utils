from __future__ import annotations

from pathlib import Path
from typing import Union
from uuid import uuid4

from . import default_serialize_dir

import msgpack


def ensure_path(dir: Union[str, Path] = None) -> bool:
    """Ensure a directory path exists.

    Returns a bool
    """

    if not dir:
        raise ValueError("Missing input directory to validate")

    if not isinstance(dir, Path) and not isinstance(dir, str):
        raise TypeError(
            f"Invalid type for property [dir]: ({type(dir)}). Must be of type str or Path"
        )

    if isinstance(dir, str):
        dir = Path(dir)

    if not dir.exists():
        try:
            dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError as f_exc:
            return True
        except PermissionError as perm_exc:
            return False
        except Exception as exc:
            raise Exception(
                {
                    "success": False,
                    "error": f"Unhandled exception creating dir: [{dir}].",
                    "details": exc,
                }
            )

    else:
        return True


def msgpack_serialize(
    _json: dict = None, output_dir: str = default_serialize_dir, filename: str = None
) -> dict[str, Union[bool, str, dict[str, Union[str, dict]]]]:
    if not _json:
        raise ValueError("Missing Python dict data to serialize")

    if not filename:
        # log.debug(f"Missing filename. Generating a random filename.")

        filename = str(uuid4())

    if filename.endswith(".msgpack"):
        filename.replace(".msgpack", "")

    dir_exist = ensure_path(output_dir)

    filename = f"{output_dir}/{filename}"

    if _json:
        try:
            with open(f"{filename}", "wb") as outfile:
                packed = msgpack.packb(_json)
                outfile.write(packed)

            return_obj = {
                "success": True,
                "detail": {"message": f"Data serialized to file {filename}"},
            }

        except Exception as exc:
            # log.error(
            #     {"exception": "Unhandled exception writing msgpack."}, exc_info=True
            # )

            return_obj = {"success": False, "detail": {"message": f"{exc}"}}

    return return_obj


def msgpack_deserialize(
    filename: str = None,
) -> dict[str, Union[bool, str, dict[str, Union[str, dict]]]]:
    if not filename:
        raise ValueError("Must pass a file name/path to deserialize")

    if not Path(filename).exists():
        raise FileNotFoundError(f"Could not find file: {filename}")

    try:
        with open(f"{filename}", "rb") as infile:
            in_bytes = infile.read()
            unpacked = msgpack.unpackb(in_bytes)

        return_obj = {
            "success": True,
            "detail": {
                "message": f"Data deserialized from file {filename}",
                "unpacked": unpacked,
            },
        }

    except Exception as exc:
        # log.error({"exception": "Unhandled exception reading msgpack."}, exc_info=True)

        return_obj = {"success": False, "detail": {"message": f"{exc}"}}

    return return_obj
