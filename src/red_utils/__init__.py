"""!!! warning

    `red_utils` is a pet project, not meant to be used in any serious capacity. If you really want to use specific features/functions of `red_utils`,
    copy the code into your own project and rewrite it enough that it works with your app.

A collection of enhancements/utilities for modules & Python packages I use frequently. Modules are broken down into `std` and `ext`.
Modules in `red_utils.std` have no external dependencies, requiring only the Python `stdlib`. Modules in `red_utils.ext`, on the other
hand, are utilities & extensions I've written for packages like `Loguru`, `SQLAlchemy`, and `Pydantic`.
"""

from __future__ import annotations

import pkgutil
import sys

sys.path.append(".")

from . import core, domain, exc, ext, std
from .exc import CustomException
