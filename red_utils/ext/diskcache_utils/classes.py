from dataclasses import dataclass, field
from typing import Union

from .constants import default_cache_dir
from red_utils.std.dataclass_mixins import DictMixin


@dataclass
class CacheInstance(DictMixin):
    """Compose a Diskcache Cache from class parameters.

    Implement functionality from operations.py, such as get_val and set_val.
    """

    cache_dir: str | None = field(default=default_cache_dir)
    cache_name: str | None = field(default="cache.db")
    index: bool = field(default=True)
