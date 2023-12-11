from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Union

from red_utils.core.constants import CACHE_DIR
from red_utils.std.dataclass_mixins import DictMixin

from .operations import (
    check_cache,
    check_cache_key_exists,
    clear_cache,
    convert_to_seconds,
    delete_val,
    get_cache_size,
    manage_cache_tag_index,
    set_expire,
    set_val,
)
from .validators import (
    valid_key_types,
    valid_val_types,
    validate_cache,
    validate_expire,
    validate_key,
    validate_read,
    validate_retry,
    validate_tag,
    validate_tags,
    validate_val,
)

from diskcache import Cache
from diskcache.core import warnings

def default_timeout() -> int:
    timeout = convert_to_seconds(amount=24, unit="hours")
    return timeout


@dataclass
class CacheInstanceBase(DictMixin):
    """Compose a Diskcache Cache from class parameters.

    Implement functionality from operations.py, such as get_val and set_val.
    """

    cache_dir: Union[str, Path] | None = field(default=CACHE_DIR)
    index: bool = field(default=True)
    cache: Cache | None = field(default=None)
    cache_timeout: int | None = field(default_factory=default_timeout)

    def __post_init__(self):
        if isinstance(self.cache_dir, str):
            if self.cache_dir == ".":
                self.cache_dir = Path().absolute()
            else:
                self.cache_dir = Path(self.cache_dir)

    def exists(self) -> bool:
        return Path(f"{self.cache_dir}/cache.db").exists()

    @property
    def cache_path(self) -> Path:
        return Path(f"{self.cache_dir}/cache.db")

    @property
    def cache_conf_dict(self) -> dict[str, Any]:
        _config = {
            "directory": self.cache_dir,
            "timeout": self.cache_timeout,
        }

        return _config

    def init(self) -> Cache:
        """Initialize a Diskcache Cache from class parameters.

        Sets the self.cache parameter to the initialized Cache,
        and also returns Cache directly.
        """
        try:
            cache = Cache(self.cache_dir, timeout=self.cache_timeout)
            self.cache = cache

            self.manage_cache_tag_index("create")

            return cache

        except Exception as exc:
            raise Exception(f"Unhandled exception creating cache. Details: {exc}")

    def manage_cache_tag_index(self, operation: str = "create") -> None:
        """Create or delete a cache index.

        Params:
        -------
        - operation (str): The operation to perform on the cache's tag index.
            - Options: ["create", "delete"]
        """
        valid_operations: list[str] = ["create", "delete"]

        validate_cache(cache=self.cache)

        if not operation:
            raise Exception(f"Operation cannot be None.")

        try:
            match operation:
                case "create":
                    if self.cache.tag_index == 0:
                        self.cache.create_tag_index()
                    else:
                        pass

                case "delete":
                    if self.cache.tag_index == 1:
                        self.cache.drop_tag_index()
                    else:
                        pass

                case _:
                    raise ValueError(
                        f"Invalid operation: {operation}. Must be one of {valid_operations}"
                    )

        except Exception as exc:
            raise Exception(
                f"Unhandled exception configuring tag_index. Details: {exc}"
            )

    def clear(self) -> bool:
        """Clear the entire cache.

        Returns a bool for success (True) or failure (False) clearing the cache.
        """
        validate_cache(self.cache)

        try:
            with self.cache as ref:
                ref.clear()

                return True

        except Exception as exc:
            raise Exception(
                f"Unhandled exception clearing cache at {self.cache.directory}. Details: {exc}"
            )


@dataclass
class CacheInstance(CacheInstanceBase):
    """Class to control a Diskcache Cache instance.

    Params:
    -------
    - cache_dir (str|Path): Directory path where cache.db will be stored.
    - index (bool): Controls creation of a tag index in the cache instance.
    - cache (diskcache.Cache): A diskcache.Cache object. When the class is instantiated, a Cache will be created.
    - cache_timeout(int): Default key expiration (in seconds).
    """

    def check_key_exists(self, key: valid_key_types = None) -> bool:
        """Check if a key exists in a cache."""
        ## Key validation
        validate_key(key=key)
        validate_cache(cache=self.cache)

        ## Check if key exists in cache
        if key in self.cache:
            return True
        else:
            return False

    def set_val(
        self,
        key: valid_key_types = None,
        val: valid_val_types = None,
        expire: int = None,
        read: bool = False,
        tag: str = None,
        retry: bool = False,
    ) -> None:
        """Set a key value pair in the cache.

        Handles optional properties like expiration, tag, retry, etc.
        """
        validate_key(key)
        validate_val(val)
        validate_expire(expire, none_ok=True)
        validate_read(read, none_ok=True)
        validate_tag(tag=tag, none_ok=True)
        validate_retry(retry=retry, none_ok=True)
        validate_cache(cache=self.cache)

        try:
            with self.cache as ref:
                ref.set(
                    key=key, value=val, expire=expire, read=read, tag=tag, retry=retry
                )

        except Exception as exc:
            raise Exception(
                f"Unhandled exception setting key/value pair for key: [{key}]. Details: {exc}"
            )

    def get_val(self, key: valid_key_types = None, tags: list[str] = None):
        """Search for a key in a given cache.

        Pass a diskcache.Cache object for cache, and a key (and optionally a list of tags).
        Function will search the cache and return a value if found, or a structured
        error dict describing the lack of key.
        """
        validate_key(key)
        validate_cache(self.cache)
        validate_tags(tags)

        try:
            if check_cache_key_exists(key=key, cache=self.cache):
                try:
                    with self.cache as ref:
                        _val = ref.get(key=key)

                        return _val

                except Exception as exc:
                    raise Exception(
                        f"Unhandled exception retrieving value of key [{key}]. Details: {exc}"
                    )

            else:
                return {
                    "error": "Key not found in cache",
                    "details": {"key": key, "cache_dir": self.cache.directory},
                }

        except Exception as exc:
            return {
                "error": "Error searching for key in cache",
                "details": {"exception": exc},
            }

    def set_expire(
        self, key: valid_key_types = None, expire: int = None
    ) -> Union[dict[str, str], None]:
        """Set an expiration timeout (in seconds).

        Params:
        -------
        - key (str): Name of the key to set expiration on. Must already exist in the cache.
        - expire (int): Time (in seconds) to wait before expiring cached value.
        """
        validate_key(key)
        validate_cache(self.cache)
        validate_expire(expire)

        if not check_cache_key_exists(key=key, cache=self.cache):
            return {
                "warning": f"Cache item with key [{key}] does not exist in cache at {self.cache.directory}/"
            }

        try:
            with self.cache as ref:
                ref.touch(key, expire=expire)

        except Exception as exc:
            raise Exception(
                f"Unhandled exception setting expiration of {expire} on key [{key}] in cache at {self.cache.directory}/. Details: {exc}"
            )

    def delete_val(self, key: valid_key_types = None, tag: str = None) -> tuple:
        """Delete a cached value.

        If a tag is provided, only keys that also have that tag will be deleted.

        Params:
        -------
        - key (str|int): Name of key in cache.
        """
        validate_key(key)
        validate_cache(self.cache)
        validate_tag(tag)

        try:
            with self.cache as ref:
                _delete = ref.pop(key=key, tag=tag)

                return _delete

        except Exception as exc:
            raise Exception(
                f"Unhandled exception deleting key {key} from cache at {self.cache.directory}/. Details: {exc}"
            )

    def get_cache_size(self) -> dict[str, int]:
        """Get a dict describing the size of the cache, in bytes.

        Return object is a dict with keys: 'unit', 'size'. Example return object:
            {'unit': 'bytes', 'size': 36864}
        """
        validate_cache(cache=self.cache)

        try:
            cache_size: int = self.cache.volume()

            return {"unit": "bytes", "size": cache_size}

        except Exception as exc:
            raise Exception(f"Unhandled exception getting cache size. Details: {exc}")

    def check_cache(self) -> list[warnings.WarningMessage]:
        """Run checks on Cache instance.

        Returns a list of Diskcache WarningMessage objects.
        """
        validate_cache(cache=self.cache)

        try:
            warnings = self.cache.check()

            return warnings

        except Exception as exc:
            raise Exception(
                f"Unhandled exception checking cache for warnings. Details: {exc}"
            )
