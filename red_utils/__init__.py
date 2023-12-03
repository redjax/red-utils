from __future__ import annotations

import pkgutil
import sys

sys.path.append(".")

from . import domain, exc, ext, std, core
from .exc import CustomException
