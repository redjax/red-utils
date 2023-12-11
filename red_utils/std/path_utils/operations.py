from __future__ import annotations

from datetime import datetime
import json

from pathlib import Path
import shutil
from typing import Any, Union

from red_utils.core.constants import JSON_DIR

def file_ts(fmt: str = "%Y-%m-%d_%H:%M:%S") -> str:
    """Return a formatted timestamp, useful for prepending to dir/file names."""
    now: str = datetime.now().strftime(fmt)

    return now


def export_json(
    input: Union[str, list[list, dict], dict[str, Any]] = None,
    output_dir: str = JSON_DIR,
    output_filename: str = f"{file_ts()}_unnamed_json.json",
):
    """Export JSON object to an output file.

    Params:
    -------
    - input (str|list[list,dict]|dict[str,Any]): The input object to be output to a file.
    - output_dir (str): The directory where a .json file will be saved.
    - output_filename (str): The name of the file that will be saved in output_dir.
    """
    if not Path(output_dir).exists():
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    if isinstance(input, dict):
        input = json.dumps(input)

    if Path(f"{output_dir}/{output_filename}").exists():
        raise FileExistsError(
            f"JSON file already exists: {output_dir}/{output_filename}"
        )

    if output_dir.endswith("/"):
        output_dir = output_dir[:-1]

    if not output_filename.endswith(".json"):
        output_filename = f"{output_filename}.json"

    output_path: str = f"{output_dir}/{output_filename}"

    print(f"Output path: {output_path}")

    if not Path(output_path).exists():
        try:
            with open(output_path, "w+") as f:
                f.write(input)
        except FileExistsError as file_exists_exc:
            raise FileExistsError(file_exists_exc)
        except FileNotFoundError as file_not_found_exc:
            raise FileNotFoundError(file_not_found_exc)
        except Exception as exc:
            raise Exception(
                f"Unhandled exception writing JSON to file: {output_path}. Details: {exc}"
            )


def crawl_dir(
    in_dir: Union[str, Path] = None,
    return_type: str = "all",
    ext_filter: str | None = None,
    files: list[Path] | None = None,
    dirs: list[Path] | None = None,
) -> dict[str, list[Path]]:
    """Crawl a directory for sub-directories/files. Continue crawl on new subdirectory.

    Parameters
    ----------
        in_dir (str | Path): An input directory to start the crawl at.
        return_type (str): Return "files", "dirs", or "all"
        ext_filter (str): Set a filetype filter, only return files matching ext
            (i.e. "csv" or ".csv")
        files (list[Path]): A list of Path objects to append found files to.
        dirs (list[Path]): A list of Path objects to append found dirs to.

    Returns
    -------
        A dict object of file and dir lists. return_obj['files'] will be a list of files
        found in path, including in subdirectories. return_obj['dirs'] will be a list of
        dirs and subdirs found during crawl.
    """
    valid_return_types: list[str] = ["all", "files", "dirs"]
    if not return_type:
        return_type = "all"

    if not isinstance(return_type, str):
        raise TypeError(f"return_type must be a string")

    return_type = return_type.lower()

    if return_type not in valid_return_types:
        raise ValueError(
            f"Invalid return type: {return_type}. Must be one of {valid_return_types}"
        )

    if ext_filter is not None:
        if not ext_filter.startswith("."):
            ext_filter = f".{ext_filter}"

    if not in_dir:
        raise ValueError(f"Missing input directory to crawl")

    if not isinstance(in_dir, Path):
        if not isinstance(in_dir, str):
            raise TypeError(
                f"Invalid type for input directory: {type(in_dir)}. Must be a str or Path object."
            )
        elif isinstance(in_dir, str):
            in_dir: Path = Path(in_dir)
        else:
            raise Exception(
                f"Unhandled exception parsing input directory. Could not detect type of in_dir."
            )

    ## Create files/dirs lists if they do not exist at function call.
    if not files:
        files = []
    if not dirs:
        dirs = []

    try:
        if ext_filter:
            search_str: str = f"**/*{ext_filter}"
        else:
            search_str: str = "**/*"

        ## Loop over in_dir
        for _f in in_dir.glob(search_str):
            if _f.is_file():
                ## Append file to files list, if it does not already exist in the list
                if _f not in files:
                    files.append(_f)
            elif _f.is_dir():
                ## Append dir to dirs list, if it does not already exist in the list
                if _f not in dirs:
                    dirs.append(_f)

                ## Re-crawl on new directory
                crawl_dir(in_dir=_f, files=files, dirs=dirs)

    except FileNotFoundError as fnf_exc:
        raise FileNotFoundError(f"Path does not exist: {in_dir}. Details: {fnf_exc}")
    except PermissionError as perm_exc:
        raise PermissionError(
            f"Encountered permission error while scanning {in_dir}. Details: {perm_exc}"
        )
    except Exception as exc:
        raise Exception(f"Unhandled exception crawling path: {in_dir}. Details: {exc}")

    return_obj: dict[str, list[Path]] = {"files": files, "dirs": dirs}

    return return_obj


def list_files(
    in_dir: str = None, ext_filter: str = None, return_files: list[Path] = []
) -> list[Path]:
    """Return list of all files in a path, optionally filtering by file extension."""
    if not in_dir:
        raise ValueError("Missing input directory to search")
    if ext_filter is not None:
        if not ext_filter.startswith("."):
            ext_filter = f".{ext_filter}"

    if ext_filter:
        search_str: str = f"**/*{ext_filter}"
    else:
        search_str: str = "**/*"

    return_files: list[Path] = []

    try:
        for _p in Path(in_dir).glob(search_str):
            if _p.is_file():
                return_files.append(_p)
            elif _p.is_dir():
                list_files(in_dir=_p, ext_filter=ext_filter, return_files=return_files)

        return return_files

    except FileNotFoundError as fnf:
        raise FileNotFoundError(f"Could not find input path: {in_dir}. Details: {fnf}")
    except PermissionError as perm:
        raise PermissionError(f"Could not open path: {in_dir}. Details: {perm}")
    except Exception as exc:
        raise Exception(
            f"Unhandled exception looping input path: {in_dir}. Details: {exc}"
        )


def ensure_dirs_exist(ensure_dirs: list[Union[str, Path]] = None) -> None:
    """Loop over a list of directories and create any paths that do not already exist.

    Params:
    -------
    - ensure_dirs (list[str]|list[Path]): A list of directory paths formatted as strings or Path objects.
        If any list item is of type str, it will be converted to a Path.
    """
    if not ensure_dirs:
        raise ValueError("Missing list of directories to ensure existence")

    validated_list: list[Path] = []

    for i in ensure_dirs:
        if isinstance(i, str):
            i = Path(i)
            validated_list.append(i)
        elif isinstance(i, Path):
            validated_list.append(i)
        else:
            print(
                ValueError(
                    f"Invalid type for list item: ({type(i)}). Must be of type str or Path."
                )
            )
            pass

    ensure_dirs = validated_list

    for d in ensure_dirs:
        if not d.exists():
            try:
                d.mkdir(exist_ok=True, parents=True)
            except Exception as exc:
                print(
                    Exception(
                        f"Unhandled exception creating directory: {d}. Details: {exc}"
                    )
                )
                pass


def delete_path(rm_path: Union[str, Path] = None) -> bool:
    """Recursively delete a path."""
    if rm_path is None:
        raise ValueError("Missing a path to remove.")
    if isinstance(rm_path, str):
        rm_path: Path = Path(rm_path)

    try:
        if rm_path.is_file():
            rm_path.unlink()
        elif rm_path.is_dir():
            shutil.rmtree(rm_path)

        return True

    except FileNotFoundError as fnf:
        print(FileNotFoundError(f"Could not find file {str(rm_path)}. Details: {fnf}"))

        return False
    except PermissionError as perm:
        print(
            PermissionError(
                f"Insufficient permissions to delete file {str(rm_path)}. Details: {perm}"
            )
        )

        return False
    except Exception as exc:
        print(
            Exception(
                f"Unhandled exception deleting file {str(rm_path)}. Details: {exc}"
            )
        )

        return False
