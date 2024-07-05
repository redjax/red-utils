"""Utilities & methods for interacting with the `DiskCache` library."""

from __future__ import annotations

from . import controllers, validators
from .__defaults import (
    CACHE_DIR,
    DEFAULT_CACHE_TIMEOUT,
    TimeoutConf,
    default_cache_conf,
    default_timeout_dict,
)
from .__methods import (
    check_cache,
    check_cache_key_exists,
    clear_cache,
    convert_to_seconds,
    delete_val,
    get_cache_size,
    get_val,
    manage_cache_tag_index,
    new_cache,
    set_expire,
    set_val,
)
from .classes import CacheInstance
from .constants import TimeoutConf
from .controllers import DiskCacheController, FanoutDiskCacheController
