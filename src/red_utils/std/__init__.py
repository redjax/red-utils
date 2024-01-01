"""
Utilities that rely only on the Python `stdlib`. Any module in this package should be safe to import & use without external dependencies.

**TODO**: Write tests to ensure `red_utils.std` can be run successfully with no dependencies.
"""
from __future__ import annotations

from . import (
    context_managers,
    dict_utils,
    hash_utils,
    path_utils,
    sqlite_utils,
    time_utils,
    uuid_utils,
)
