from __future__ import annotations

import pytest

pytest_plugins = [
    "tests.fixtures.std.path_fixtures",
    "tests.fixtures.std.dict_fixtures",
    "tests.fixtures.std.hash_fixtures",
    "tests.fixtures.std.uuid_fixtures",
    "tests.fixtures.ext.time_fixtures",
    "tests.fixtures.ext.sqla_fixtures",
]
