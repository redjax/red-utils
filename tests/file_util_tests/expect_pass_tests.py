"""Tests designed to pass when run with pytest.

These tests expect assertions to be True, and will crash pytest if assertions fail.
"""
from __future__ import annotations

import datetime

from pathlib import Path

from red_utils import file_utils

from pytest import mark, xfail

@mark.file_utils
def test_cwd_exists(cwd: Path):
    """Test the CWD fixture."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"
    assert cwd.exists(), "CWD must exist."


@mark.file_utils
def test_ts(file_ts: str):
    """Test the file timestamp string fixture."""
    assert file_ts is not None, "File timestamp cannot be None."
    assert isinstance(
        file_ts, str
    ), f"Timestamp must be a string, not ({type(file_ts)})"


@mark.file_utils
def test_crawl_all(cwd: Path):
    """Test a recursive crawl of all files/dirs in CWD."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    all_crawl: dict[str, list[Path]] = file_utils.crawl_dir(in_dir=cwd)

    assert isinstance(
        all_crawl, dict
    ), f"Crawl response should be a dict, not ({type(all_crawl)})"


@mark.file_utils
def test_crawl_files(cwd: Path):
    """Test a recursive crawl of only files in CWD."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    file_crawl: dict[str, list[Path]] = file_utils.crawl_dir(
        in_dir=cwd, return_type="files"
    )

    assert isinstance(
        file_crawl, dict
    ), f"File crawl response should be a dict, not ({type(file_crawl)})"


@mark.file_utils
def test_crawl_dirs(cwd: Path):
    """Test a recursive crawl of only dirs in CWD."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    dir_crawl: dict[str, list[Path]] = file_utils.crawl_dir(
        in_dir=cwd, return_type="dirs"
    )

    assert isinstance(
        dir_crawl, dict
    ), f"Dir crawl response should be a dict, not ({type(dir_crawl)})"


@mark.file_utils
def test_crawl_dir_for_py_filetype(cwd: Path):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    py_crawl: dict[str, list[Path]] = file_utils.crawl_dir(
        in_dir=cwd, return_type="files", ext_filter=".py"
    )

    assert isinstance(
        py_crawl, dict
    ), f".py file crawl response should be a dict, not ({type(py_crawl)})"

    for f in py_crawl["files"]:
        assert f.is_file(), f"File should have been a file"
        assert f.suffix == ".py", f"Filetype should have been .py, not {f.suffix}"


@mark.file_utils
def test_list_files(cwd: Path):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    file_list: list[Path] = file_utils.list_files(in_dir=cwd)

    assert isinstance(
        file_list, list
    ), f"List of files should have been a list of Path objects, not {type(file_list)}"

    for _p in file_list:
        assert isinstance(
            _p, Path
        ), f"File object should have been a pathlib.Path object, not {type(_p)}"
        assert _p.is_file(), "File must be a file Path-type object"


@mark.file_utils
def test_list_files_py_filetype(cwd: Path):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    file_list: list[Path] = file_utils.list_files(in_dir=cwd, ext_filter="py")

    assert isinstance(
        file_list, list
    ), f"List of files should have been a list of Path objects, not {type(file_list)}"

    for _p in file_list:
        assert isinstance(
            _p, Path
        ), f"File object should have been a pathlib.Path object, not {type(_p)}"
        assert _p.is_file(), "File must be a file Path-type object"
        assert (
            _p.suffix == ".py"
        ), f"File extension should have been .py, not {_p.suffix}"
