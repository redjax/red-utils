from __future__ import annotations

import pkgutil

"""Use pkgutil to only load modules if dependencies are met.

This keeps the red_utils package functional by limiting the utilities that are loaded.
If a pkgutil.find_loader() check fails, that import is passed over and will be unavailable
for type completion & usage.
"""


if pkgutil.find_loader("arrow") or pkgutil.find_loader("pendulum"):
    from . import time_utils

if pkgutil.find_loader("loguru"):
    from . import loguru_utils

if pkgutil.find_loader("pydantic"):
    from . import pydantic_utils

if pkgutil.find_loader("msgpack"):
    from . import msgpack_utils

if pkgutil.find_loader("diskcache"):
    from . import diskcache_utils

if pkgutil.find_loader("httpx"):
    from . import httpx_utils

if pkgutil.find_loader("fastapi"):
    from . import fastapi_utils

if pkgutil.find_loader("sqlalchemy"):
    from . import sqlalchemy_utils

if pkgutil.find_loader("rich"):
    from . import context_managers

if pkgutil.find_loader("pandas") or pkgutil.find_loader("polars"):
    from . import dataframe_utils
