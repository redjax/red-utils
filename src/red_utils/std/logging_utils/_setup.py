from __future__ import annotations

from copy import deepcopy
import logging
import logging.config
import typing as t

log = logging.getLogger("red_utils.std.logging_utils.setup")

from red_utils.std.logging_utils._methods import merge_config_dicts
from red_utils.std.logging_utils.fmts._formats import (
    DATE_FMT_STANDARD,
    MESSAGE_FMT_DETAILED,
    MESSAGE_FMT_STANDARD,
)


def setup_logging(
    app_name: str = "app",
    log_level: str = "DEBUG",
    merge_logging_formatters: list[dict] | None = None,
    merge_logging_handlers: list[dict] | None = None,
    merge_logging_loggers: list[dict] | None = None,
    merge_logging_configs: list[dict] | None = None,
):
    """Initialize Python's standard logging module.

    This method uses my personal preferred log message formats and other defaults. You may want to just reference
    the logging_config dict in this method and create your own logging setup method based on this one.
    """
    # Define default logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": MESSAGE_FMT_STANDARD,
                "datefmt": DATE_FMT_STANDARD,
            },
            "detail": {
                "format": MESSAGE_FMT_DETAILED,
                "datefmt": DATE_FMT_STANDARD,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            app_name: {
                "handlers": ["console"],
                "level": log_level.upper(),
                "propagate": False,
            },
            "notebook": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    # Merge extra formatters
    if merge_logging_formatters:
        for formatter in merge_logging_formatters:
            try:
                logging_config["formatters"].update(formatter)
            except Exception as exc:
                logging.error(f"Error merging extra formatter: {exc}")

    # Merge extra handlers
    if merge_logging_handlers:
        for handler in merge_logging_handlers:
            try:
                logging_config["handlers"].update(handler)
            except Exception as exc:
                logging.error(f"Error merging extra handler: {exc}")

    # Merge extra loggers
    if merge_logging_loggers:
        for logger in merge_logging_loggers:
            try:
                logging_config["loggers"].update(logger)
            except Exception as exc:
                logging.error(f"Error merging extra logger: {exc}")

    # Merge additional logging configurations
    if merge_logging_configs:
        merged_config = deepcopy(logging_config)
        for config in merge_logging_configs:
            try:
                merged_config = merge_config_dicts(merged_config, config)
            except Exception as exc:
                logging.error(f"Error merging logging configs: {exc}")
                break
        else:
            logging_config = merged_config

    # Configure logging
    try:
        logging.config.dictConfig(logging_config)
    except Exception as exc:
        logging.error(f"Error configuring logging: {exc}")
        raise exc
