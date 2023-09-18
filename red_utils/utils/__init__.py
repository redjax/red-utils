from __future__ import annotations

import pkgutil

from .stdlib_utils import (
    context_managers,
    dict_utils,
    file_utils,
    hash_utils,
    time_utils,
    uuid_utils,
)

## Use pkgutil to only load modules
#  if dependencies are met
if pkgutil.find_loader("arrow"):
    from .extended_utils import arrow_utils

if pkgutil.find_loader("pendulum"):
    from .extended_utils import pendulum_utils

if pkgutil.find_loader("loguru"):
    from .extended_utils import loguru_utils

if pkgutil.find_loader("pydantic"):
    from .extended_utils import pydantic_utils

if pkgutil.find_loader("msgpack"):
    from .extended_utils import msgpack_utils

if pkgutil.find_loader("diskcache"):
    from .extended_utils import diskcache_utils

if pkgutil.find_loader("httpx"):
    from .extended_utils import httpx_utils

if pkgutil.find_loader("fastapi"):
    from .extended_utils import fastapi_utils

if pkgutil.find_loader("sqlalchemy"):
    from .extended_utils import sqlalchemy_utils
