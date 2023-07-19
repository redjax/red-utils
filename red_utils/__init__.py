from __future__ import annotations

## Import modules with only stdblit dependencies directly
from .context_managers import benchmark, async_benchmark, ListProtect, DictProtect
from .file_utils import default_json_dir, ts, export_json, crawl_dir
from .dict_utils import validate_dict, debug_dict, merge_dicts, update_dict
from .hash_utils import get_hash_from_str
from .uuid_utils import (
    UUIDLength,
    glob_uuid_lens,
    gen_uuid,
    trim_uuid,
    first_n_chars,
    get_rand_uuid,
)
from .time_utils import (
    default_format as default_ts_format,
    twelve_hour_format as ts_twelve_hour_format,
    datetime_as_dt,
    datetime_as_str,
    get_ts,
)

## Use try/except to import modules with dependencies
#  Keeps program from crashing when only a single module
#    is missing a depenency.
try:
    from . import diskcache_utils
except:
    pass
try:
    from . import httpx_utils
except:
    pass
try:
    from . import loguru_utils
except:
    pass
try:
    from . import msgpack_utils
except:
    pass

## Only import fastapi utils if fastapi and uvicorn are installed
try:
    from . import fastapi_utils
except:
    pass
