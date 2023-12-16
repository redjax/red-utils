"""Tests designed to fail when run with pytest.

These tests are marked with xfail, and assert conditions that will always fail. Because they are marked xfail,
these tests will not stop pytest execution.
"""
from __future__ import annotations

import datetime

from pathlib import Path

from red_utils import file_utils

from pytest import mark, xfail

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
