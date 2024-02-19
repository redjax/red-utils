from __future__ import annotations

from pathlib import Path

from pytest import fixture
from red_utils.std import path_utils

@fixture
def cwd() -> Path:
    """Create a fixture of the current working directory.

    Useful for testing path/file functions.
    """
    _cwd: Path = Path("src/red_utils")

    return _cwd


@fixture
def file_ts() -> str:
    _ts = path_utils.file_ts()

    return _ts
