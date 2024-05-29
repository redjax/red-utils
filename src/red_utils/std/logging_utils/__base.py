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
