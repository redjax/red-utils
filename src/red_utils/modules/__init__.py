from red_utils._importer import module_installed, raise_import_err

from .std import (
    path_utils,
    context_managers,
    dict_utils,
    hash_utils,
    list_utils,
    sqlite_utils,
    time_utils,
    uuid_utils,
)


def method_name():
    pass


# loguru_utils
if module_installed("loguru"):
    from . import loguru_utils
else:
    pass
    # loguru_utils = None

# pydantic_utils
if module_installed("pydantic"):
    from . import pydantic_utils
else:
    pass
    # pydantic_utils = None

if module_installed("httpx"):
    from . import httpx_utils
else:
    pass
    # httpx_utils = None
