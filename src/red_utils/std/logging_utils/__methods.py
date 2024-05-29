import logging

log = logging.getLogger("red_utils.std.logging_utils")

from copy import deepcopy
import typing as t
from pathlib import Path

from red_utils.std.logging_utils.__base import BASE_LOGGING_CONFIG_DICT
from red_utils.std.logging_utils.fmts import (
    MESSAGE_FMT_BASIC,
    MESSAGE_FMT_DETAILED,
    MESSAGE_FMT_STANDARD,
    DATE_FMT_DATE_ONLY,
    DATE_FMT_STANDARD,
    DATE_FMT_TIME_ONLY,
)
from red_utils.std.logging_utils.fmts import RED_UTILS_DETAIL_FMT, RED_UTILS_FMT
from red_utils.std.logging_utils.config_classes.handlers import (
    RotatingFileHandlerConfig,
    StreamHandlerConfig,
    FileHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
    SocketHandlerConfig,
    TimedRotatingFileHandlerConfig,
)
from red_utils.std.logging_utils.config_classes.formatters import FormatterConfig
from red_utils.std.logging_utils.config_classes.loggers import (
    LoggerConfig,
    LoggerFactory,
)
from red_utils.std.logging_utils.config_classes.types import (
    HANDLER_CLASSES_TYPE,
    LOGGING_CONFIG_DICT_TYPE,
    HANDLER_CLASSES_TYPE_ANNOTATION,
    LOGGING_CONFIG_DICT_TYPE_ANNOTATION,
)


def _ensure_logdir(p: t.Union[str, Path] = None) -> None:
    p: Path = Path(f"{p}")
    if "~" in f"{p}":
        p = p.expanduser()

    if not p.exists():
        try:
            p.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception creating directory '{p}'. Details: {exc}"
            )
            log.error(msg)

            raise exc
    else:
        return


def get_rotatingfilehandler_config(
    name: str = "rotating_app_file",
    level: str = "DEBUG",
    formatter: str = "default",
    filters: list | None = None,
    filename: t.Union[str, Path] = None,
    maxBytes: int = 100000,
    backupCount: int = 3,
    as_dict: bool = False,
) -> dict[str, dict[str, t.Any]] | RotatingFileHandlerConfig:
    filename: Path = Path(f"{filename}")
    if "~" in f"{filename}":
        filename = filename.expanduser()

    _ensure_logdir(p=filename.parent)

    try:
        _handler: RotatingFileHandlerConfig = RotatingFileHandlerConfig(
            name=name,
            level=level,
            formatter=formatter,
            filters=filters,
            filename=filename,
            maxBytes=maxBytes,
            backupCount=backupCount,
        )

        if as_dict:
            return _handler.get_configdict()
        else:
            return _handler

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception building RotatingFileHandlerConfig. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_streamhandler_config(
    name: str = "console",
    level: str = "INFO",
    formatter: str = "default",
    filters: list | None = None,
    stream: str = "ext://sys.stdout",
    as_dict: bool = False,
) -> dict[str, dict[str, str]] | StreamHandlerConfig:
    try:
        _handler: StreamHandlerConfig = StreamHandlerConfig(
            name=name, level=level, formatter=formatter, filters=filters, stream=stream
        )

        if as_dict:
            return _handler.get_configdict()
        else:
            return _handler

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception building StreamHandlerConfig. Details: {exc}"
        )
        log.error(msg)

        raise exc


def get_formatter_config(
    name: str = "default",
    fmt: str = MESSAGE_FMT_STANDARD,
    datefmt: str = DATE_FMT_STANDARD,
    style: str = "%",
    validate: bool = True,
    as_dict: bool = False,
) -> dict[str, dict[str, str]] | FormatterConfig:
    try:
        _formatter: FormatterConfig = FormatterConfig(
            name=name, fmt=fmt, datefmt=datefmt, style=style, validate=validate
        )

        if as_dict:
            return _formatter.get_configdict()
        else:
            return _formatter
    except Exception as exc:
        msg = Exception(f"Unhandled exception building FormatterConfig. Details: {exc}")
        log.error(msg)

        raise exc


def get_logger_config(
    name: str = "app",
    handlers: list[str] = ["console"],
    level: str = "DEBUG",
    propagate: bool = False,
) -> dict[str, dict[str, str]] | LoggerConfig:
    try:
        _logger: LoggerConfig = LoggerConfig(
            name=name, level=level.upper(), handlers=handlers, propagate=propagate
        )

        return _logger

    except Exception as exc:
        msg = Exception(f"Unhandled exception initializing logger. Details: {exc}")
        log.error(msg)

        raise exc


def assemble_configdict(
    disable_existing_loggers: bool = False,
    propagate: bool = False,
    root_handlers: list[str] = ["console"],
    root_level: str = "DEBUG",
    formatters: (
        t.Union[list[FormatterConfig], list[LOGGING_CONFIG_DICT_TYPE_ANNOTATION]] | None
    ) = None,
    handlers: (
        t.Union[HANDLER_CLASSES_TYPE_ANNOTATION, LOGGING_CONFIG_DICT_TYPE_ANNOTATION]
        | None
    ) = None,
    loggers: (
        t.Union[
            list[t.Union[LoggerConfig, LoggerFactory]],
            list[LOGGING_CONFIG_DICT_TYPE_ANNOTATION],
        ]
        | None
    ) = None,
):
    """Build a logging dictConfig dict.

    ```python title="Example logging config dict" linenums="1"
    logging_config: dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "propagate": True,
        "root": {},
        "formatters": {},
        "handlers": {},
        "loggers": {},
    }
    ```

    """
    logging_config: dict = BASE_LOGGING_CONFIG_DICT

    logging_config["disable_existing_loggers"] = disable_existing_loggers
    logging_config["propagate"] = propagate

    config_key_root = {
        ## Set handlers
        "handlers": root_handlers,
        ## Set log level string
        "level": root_level.upper(),
    }

    logging_config["root"] = config_key_root

    formatter_configdicts: LOGGING_CONFIG_DICT_TYPE = {}
    handler_configdicts: LOGGING_CONFIG_DICT_TYPE = {}
    logger_configdicts: LOGGING_CONFIG_DICT_TYPE = {}

    if formatters is not None:
        for formatter_dict in formatters:
            if isinstance(formatter_dict, dict):
                pass
            elif isinstance(formatter_dict, FormatterConfig):
                formatter_dict: dict = formatter_dict.get_configdict()

            formatter_configdicts.update(formatter_dict)

    if handlers is not None:
        for handler_dict in handlers:
            if isinstance(handler_dict, dict):
                pass
            elif isinstance(handler_dict, HANDLER_CLASSES_TYPE):
                handler_dict = handler_dict.get_configdict()

            handler_configdicts.update(handler_dict)

    if loggers:
        for logger_dict in loggers:
            if isinstance(logger_dict, dict):
                pass
            elif isinstance(logger_dict, LoggerConfig):
                logger_dict = logger_dict.get_configdict()

            logger_configdicts.update(logger_dict)

    return_dict = deepcopy(logging_config)

    return_dict["formatters"] = formatter_configdicts
    return_dict["handlers"] = handler_configdicts
    return_dict["loggers"] = logger_configdicts

    return return_dict
