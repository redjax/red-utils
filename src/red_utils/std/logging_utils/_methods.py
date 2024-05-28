from __future__ import annotations

from copy import deepcopy
import logging
import typing as t

log = logging.getLogger("red_log.std.logging_utils")


def merge_config_dicts(configdict1: dict = None, configdict2: dict = None):
    merged_config = deepcopy(configdict1)

    def _merge_dicts(d1, d2):
        for key, value in d2.items():
            if key in d1:
                if isinstance(d1[key], dict) and isinstance(value, dict):
                    _merge_dicts(d1[key], value)
                elif isinstance(d1[key], list) and isinstance(value, list):
                    d1[key].extend(value)
                else:
                    # Handle conflict if necessary or just overwrite
                    d1[key] = value
            else:
                d1[key] = value

    try:
        _merge_dicts(merged_config, configdict2)
        return merged_config
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception merging config dicts. Returning original dict. Details: {exc}"
        )
        log.error(msg)

        return configdict1


def return_logging_config_dict() -> dict[str, t.Any]:
    """Reconstruct the logging configuration dictionary from the current logging setup."""
    raise NotImplementedError("This function doesn't work and is being revised.")
    config: dict[str, t.Any] = {
        "version": 1,
        "disable_existing_loggers": logging.root.manager.disable,
        "formatters": {},
        "handlers": {},
        "loggers": {},
    }

    formatter_name = "standard"  # Define a default formatter name

    # Collect all formatters and handlers from all loggers
    for logger in logging.root.manager.loggerDict.values():
        if isinstance(logger, logging.Logger):
            for handler in logger.handlers:
                # Formatters
                if handler.formatter and formatter_name not in config["formatters"]:
                    formatter_name = handler.formatter._fmt
                    config["formatters"][formatter_name] = {
                        "format": handler.formatter._fmt,
                        "datefmt": handler.formatter.datefmt,
                    }

                # Handlers
                handler_name = (
                    handler.get_name() if hasattr(handler, "get_name") else str(handler)
                )
                if handler_name not in config["handlers"]:
                    config["handlers"][handler_name] = {
                        "class": f"{handler.__module__}.{handler.__class__.__name__}",
                        "level": logging.getLevelName(handler.level),
                        "formatter": formatter_name,
                        "stream": (
                            handler.stream.name if hasattr(handler, "stream") else None
                        ),
                    }

    # Collect loggers
    for name, logger in logging.root.manager.loggerDict.items():
        if isinstance(logger, logging.Logger):
            config["loggers"][name] = {
                "level": logging.getLevelName(logger.level),
                "handlers": [
                    handler.get_name() if hasattr(handler, "get_name") else str(handler)
                    for handler in logger.handlers
                ],
                "propagate": logger.propagate,
            }

    # Add root logger to the config
    root_logger = logging.getLogger()
    config["loggers"][""] = {
        "level": logging.getLevelName(root_logger.level),
        "handlers": [
            handler.get_name() if hasattr(handler, "get_name") else str(handler)
            for handler in root_logger.handlers
        ],
        "propagate": root_logger.propagate,
    }

    return config
