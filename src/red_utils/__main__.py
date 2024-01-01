"""
This module exists to warn a user if they ever call the `red_utils` module directly.

`red_utils` was not meant to be imported directly, the user is meant to import modules, like `from red_utils.std.path_utils import crawl_dir` (or `red_utils.std import path_utils`).
"""
from __future__ import annotations

import sys

sys.path.append(".")

warning_msg: str = """
[WARNING]
This module was not meant to be run directly.
You should import utility modules from it.

Example imports:
    from red_utils.utils import diskcache_utils, dict_utils
    from red_utils import CompatibleUUID
"""

if __name__ == "__main__":
    print(warning_msg)
