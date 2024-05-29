"""Stores a base logging config dict in `BASE_LOGGING_CONFIG_DICT`.

This can be imported and updated to create a valid logging dictConfig.
"""

import typing as t

BASE_LOGGING_CONFIG_DICT: dict[str, t.Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "propagate": True,
    "root": {},
    "formatters": {},
    "handlers": {},
    "loggers": {},
}
