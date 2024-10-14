from __future__ import annotations

from typing import Any, Union

from red_utils.core.constants import CACHE_DIR

from .__methods import convert_to_seconds
from .constants import TimeoutConf

# from .constants import default_timeout_dict

DEFAULT_CACHE_TIMEOUT: TimeoutConf = TimeoutConf()
default_timeout_dict: dict[str, Union[str, int]] = TimeoutConf().as_dict()

## Define a default cache object
default_cache_conf: dict[str, Any] = {
    "directory": CACHE_DIR,
    "timeout": convert_to_seconds(
        unit=default_timeout_dict["unit"], amount=default_timeout_dict["amount"]
    ),
}
