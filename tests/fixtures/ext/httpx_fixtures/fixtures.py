from __future__ import annotations

from pathlib import Path

from pytest import fixture
from red_utils.ext import httpx_utils


@fixture
def httpx_tmp_cache(
    CACHE_DIR: Path = Path(f"/tmp/red-utils/tests/httpx/tmpdir/cache/hishel"),
) -> Path:
    CACHE_DIR: Path = Path(f"{CACHE_DIR}")

    if CACHE_DIR.is_file():
        raise ValueError(f"Path '{CACHE_DIR}' is a file. Expected a directory path.")

    if not CACHE_DIR.exists():
        try:
            CACHE_DIR.mkdir(parents=True, exist_ok=True)
        except PermissionError as perm_err:
            print(
                f"[ERROR] Permission error creating path '{CACHE_DIR}'. Details: {perm_err}"
            )

            raise perm_err
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception creating temporary cache directory '{CACHE_DIR}'. Details: {exc}"
            )
            print(f"[ERROR] {msg}")

            raise exc

    return CACHE_DIR
