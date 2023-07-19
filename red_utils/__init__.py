from __future__ import annotations

from .context_managers import ListProtect, DictProtect

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

from .context_managers import benchmark, async_benchmark
