from pytest import fixture
from pathlib import Path
from red_utils import file_utils


@fixture
def cwd() -> Path:
    """Create a fixture of the current working directory.

    Useful for testing path/file functions.
    """
    _cwd: Path = Path("red_utils")

    return _cwd


@fixture
def file_ts() -> str:
    _ts = file_utils.constants.file_ts()

    return _ts
