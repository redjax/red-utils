from __future__ import annotations

from pathlib import Path

from pytest import mark, xfail


@mark.httpx_utils
def test_httpx_tmpdir(httpx_tmp_cache: Path):
    print(
        f"Temp cache directory: {httpx_tmp_cache}. Exists: {httpx_tmp_cache.exists()}"
    )

    if not httpx_tmp_cache.exists():
        raise FileNotFoundError(f"Could not find path '{httpx_tmp_cache}'")
    else:
        return True
