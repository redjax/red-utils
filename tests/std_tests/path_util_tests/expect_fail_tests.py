"""Tests designed to fail when run with pytest.

These tests are marked with xfail, and assert conditions that will always fail. Because they are marked xfail,
these tests will not stop pytest execution.
"""

from __future__ import annotations

import datetime
import os
from pathlib import Path

from pytest import mark, xfail
from red_utils.std import path_utils

## Tests below are expected to fail and will not raise an exception


@mark.xfail
def test_fail_crawl_cwd_none(cwd: Path = None):
    assert cwd is not None, "CWD cannot be None."


@mark.xfail
def test_fail_crawl_cwd_type(cwd: Path = "/i/do-not/exist"):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD should be of type Path, not ({type(cwd)})"


@mark.xfail
def test_fail_crawl_cwd_exists(cwd: Path = "/i/do-not/exist"):
    cwd: Path = Path(cwd)

    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD should be of type Path, not ({type(cwd)})"
    assert cwd.exists(), "CWD path should exist"


@mark.xfail
def test_fail_list_files_cwd_none(cwd: Path = None):
    assert cwd is not None, "CWD cannot be None."


@mark.xfail
def test_fail_list_files_cwd_type(cwd: Path = "/i/do-not/exist"):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD should be of type Path, not ({type(cwd)})"


@mark.xfail
def test_fail_list_files_exists(cwd: Path = "/i/do-not/exist"):
    cwd: Path = Path(cwd)

    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD should be of type Path, not ({type(cwd)})"
    assert cwd.exists(), "CWD path should exist"


@mark.file_utils
def test_fail_scan_all(cwd: Path):
    all_as_str: list[str] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=False, return_type="all"
    )
    assert all_as_str is not None, ValueError(
        "Expected failure, all_as_str should not have been None"
    )
    assert not isinstance(all_as_str, list), ValueError("Expected failure")


@mark.file_utils
def test_fail_scan_dirs(cwd: Path):
    ## Force test to fail
    dirs_as_str: list[str] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=False, return_type="all"
    )
    assert dirs_as_str is not None, ValueError(
        "Expected failure, dirs_as_str should not have been None"
    )


@mark.file_utils
def test_fail_scan_files(cwd: Path):
    ## Force test to fail
    files_as_str: list[str] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=False, return_type="all"
    )
    assert files_as_str is not None, ValueError(
        "Expected failure, files_as_str should not have been None"
    )
