"""Tests designed to pass when run with pytest.

These tests expect assertions to be True, and will crash pytest if assertions fail.
"""

from __future__ import annotations

import datetime
import os
from pathlib import Path

from red_utils.std import path_utils

from pytest import mark, xfail

@mark.path_utils
def test_cwd_exists(cwd: Path):
    """Test the CWD fixture."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"
    assert cwd.exists(), "CWD must exist."


@mark.path_utils
def test_ts(file_ts: str):
    """Test the file timestamp string fixture."""
    assert file_ts is not None, "File timestamp cannot be None."
    assert isinstance(file_ts, str), (
        f"Timestamp must be a string, not ({type(file_ts)})"
    )


@mark.path_utils
def test_scan_all(cwd: Path):
    all_as_str: list[str] = path_utils.scan_dir(
        target=cwd, as_str=True, as_pathlib=False, return_type="all"
    )
    assert all_as_str is not None, ValueError("all_as_str should not have been None")
    assert isinstance(all_as_str, list), TypeError(
        f"all_as_str should have been of type list[str]. Got type: ({type(all_as_str)})"
    )
    for i in all_as_str:
        assert isinstance(i, str), TypeError(
            f"All items in all_as_str should be of type str. Got type: ({type(i)})"
        )

    all_as_direntry: list[os.DirEntry] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=False, return_type="all"
    )
    assert all_as_direntry is not None, ValueError(
        "all_as_direntry should not have been None"
    )
    assert isinstance(all_as_direntry, list), TypeError(
        f"all_as_direntry should have been of type list[os.DirEntry]. Got type: ({type(all_as_direntry)})"
    )
    for i in all_as_direntry:
        assert isinstance(i, os.DirEntry), TypeError(
            f"All items in all_as_direntry should be of type os.DirEntry. Got type: ({type(i)})"
        )

    all_as_pathlib_path: list[Path] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=True, return_type="all"
    )
    assert all_as_pathlib_path is not None, ValueError(
        "all_as_pathlib_path should not have been None"
    )
    assert isinstance(all_as_pathlib_path, list), TypeError(
        f"all_as_pathlib_path should have been of type list[pathlib.Path]. Got type: ({type(all_as_pathlib_path)})"
    )
    for i in all_as_pathlib_path:
        assert isinstance(i, Path), TypeError(
            f"All items in all_as_pathlib_path should be of type pathlib.Path. Got type: ({type(i)})"
        )


@mark.path_utils
def test_scan_dirs(cwd: Path):
    dirs_as_str: list[str] = path_utils.scan_dir(
        target=cwd, as_str=True, as_pathlib=False, return_type="dirs"
    )
    assert dirs_as_str is not None, ValueError("dirs_as_str should not have been None")
    assert isinstance(dirs_as_str, list), TypeError(
        f"dirs_as_str should have been of type list[str]. Got type: ({type(dirs_as_str)})"
    )
    for i in dirs_as_str:
        assert isinstance(i, str), TypeError(
            f"All items in dirs_as_str should be of type str. Got type: ({type(i)})"
        )
        assert Path(i).is_dir(), ValueError(
            f"Path '{i}' should have been a directory, but was a file."
        )

    dirs_as_direntry: list[os.DirEntry] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=False, return_type="dirs"
    )
    assert dirs_as_direntry is not None, ValueError(
        "dirs_as_direntry should not have been None"
    )
    assert isinstance(dirs_as_direntry, list), TypeError(
        f"dirs_as_direntry should have been of type list[os.DirEntry]. Got type: ({type(dirs_as_direntry)})"
    )
    for i in dirs_as_direntry:
        assert isinstance(i, os.DirEntry), TypeError(
            f"All items in dirs_as_direntry should be of type os.DirEntry. Got type: ({type(i)})"
        )
        assert Path(i.path).is_dir(), ValueError(
            f"Path '{i.path}' should have been a directory, but was a file."
        )

    dirs_as_pathlib_path: list[Path] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=True, return_type="dirs"
    )
    assert dirs_as_pathlib_path is not None, ValueError(
        "dirs_as_pathlib_path should not have been None"
    )
    assert isinstance(dirs_as_pathlib_path, list), TypeError(
        f"dirs_as_pathlib_path should have been of type list[pathlib.Path]. Got type: ({type(dirs_as_pathlib_path)})"
    )
    for i in dirs_as_pathlib_path:
        assert isinstance(i, Path), TypeError(
            f"All items in dirs_as_pathlib_path should be of type pathlib.Path. Got type: ({type(i)})"
        )
        assert i.is_dir(), ValueError(
            f"Path '{i}' should have been a directory, but was a file."
        )


@mark.path_utils
def test_scan_files(cwd: Path):
    files_as_str: list[str] = path_utils.scan_dir(
        target=cwd, as_str=True, as_pathlib=False, return_type="files"
    )
    assert files_as_str is not None, ValueError(
        "files_as_str should not have been None"
    )
    assert isinstance(files_as_str, list), TypeError(
        f"files_as_str should have been of type list[str]. Got type: ({type(files_as_str)})"
    )
    for i in files_as_str:
        assert isinstance(i, str), TypeError(
            f"All items in files_as_str should be of type str. Got type: ({type(i)})"
        )
        assert Path(i).is_file(), ValueError(
            f"Path '{i}' should have been a file, but was a directory."
        )

    files_as_direntry: list[os.DirEntry] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=False, return_type="files"
    )
    assert files_as_direntry is not None, ValueError(
        "files_as_direntry should not have been None"
    )
    assert isinstance(files_as_direntry, list), TypeError(
        f"files_as_direntry should have been of type list[os.DirEntry]. Got type: ({type(files_as_direntry)})"
    )
    for i in files_as_direntry:
        assert isinstance(i, os.DirEntry), TypeError(
            f"All items in files_as_direntry should be of type os.DirEntry. Got type: ({type(i)})"
        )
        assert Path(i.path).is_file(), ValueError(
            f"Path '{i}' should have been a file, but was a directory."
        )

    files_as_pathlib_path: list[Path] = path_utils.scan_dir(
        target=cwd, as_str=False, as_pathlib=True, return_type="files"
    )
    assert files_as_pathlib_path is not None, ValueError(
        "files_as_pathlib_path should not have been None"
    )
    assert isinstance(files_as_pathlib_path, list), TypeError(
        f"files_as_pathlib_path should have been of type list[pathlib.Path]. Got type: ({type(files_as_pathlib_path)})"
    )
    for i in files_as_pathlib_path:
        assert isinstance(i, Path), TypeError(
            f"All items in files_as_pathlib_path should be of type pathlib.Path. Got type: ({type(i)})"
        )
        assert i.is_file(), ValueError(
            f"Path '{i}' should have been a file, but was a directory."
        )


@mark.path_utils
def test_crawl_all(cwd: Path):
    """Test a recursive crawl of all files/dirs in CWD."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    all_crawl: dict[str, list[Path]] = path_utils.crawl_dir(target=cwd)

    assert isinstance(all_crawl, dict), (
        f"Crawl response should be a dict, not ({type(all_crawl)})"
    )


@mark.path_utils
def test_crawl_files(cwd: Path):
    """Test a recursive crawl of only files in CWD."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    file_crawl: dict[str, list[Path]] = path_utils.crawl_dir(
        target=cwd, return_type="files"
    )

    assert isinstance(file_crawl, list), (
        f"File crawl response should be a list, not ({type(file_crawl)})"
    )


@mark.path_utils
def test_crawl_dirs(cwd: Path):
    """Test a recursive crawl of only dirs in CWD."""
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    dir_crawl: dict[str, list[Path]] = path_utils.crawl_dir(
        target=cwd, return_type="dirs"
    )

    assert isinstance(dir_crawl, list), (
        f"Dir crawl response should be a list, not ({type(dir_crawl)})"
    )


@mark.path_utils
def test_crawl_dir_for_py_filetype(cwd: Path):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    py_crawl: dict[str, list[Path]] = path_utils.crawl_dir(
        target=cwd, return_type="files", filetype_filter=".py"
    )

    assert isinstance(py_crawl, list), (
        f".py file crawl response should be a list, not ({type(py_crawl)})"
    )

    for f in py_crawl:
        assert f.is_file(), f"File should have been a file"
        assert f.suffix == ".py", f"Filetype should have been .py, not {f.suffix}"


@mark.path_utils
def test_list_files(cwd: Path):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    file_list: list[Path] = path_utils.list_files(in_dir=cwd)

    assert isinstance(file_list, list), (
        f"List of files should have been a list of Path objects, not {type(file_list)}"
    )

    for _p in file_list:
        assert isinstance(_p, Path), (
            f"File object should have been a pathlib.Path object, not {type(_p)}"
        )
        assert _p.is_file(), "File must be a file Path-type object"


@mark.path_utils
def test_list_files_py_filetype(cwd: Path):
    assert cwd is not None, "CWD cannot be None."
    assert isinstance(cwd, Path), f"CWD must be of type Path, not ({type(cwd)})"

    file_list: list[Path] = path_utils.list_files(in_dir=cwd, ext_filter="py")

    assert isinstance(file_list, list), (
        f"List of files should have been a list of Path objects, not {type(file_list)}"
    )

    for _p in file_list:
        assert isinstance(_p, Path), (
            f"File object should have been a pathlib.Path object, not {type(_p)}"
        )
        assert _p.is_file(), "File must be a file Path-type object"
        assert _p.suffix == ".py", (
            f"File extension should have been .py, not {_p.suffix}"
        )
