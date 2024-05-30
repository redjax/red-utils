"""An empty, valid/complete logging config dict.

This can be imported and added to so you can create your own logging config, and it
is also used by the `.assemble_configdict()` method as the basis for the returned logging dictConfig.
"""

from __future__ import annotations

BASE_LOGGING_CONFIG_DICT: dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {},
    "handlers": {},
    "loggers": {},
}
