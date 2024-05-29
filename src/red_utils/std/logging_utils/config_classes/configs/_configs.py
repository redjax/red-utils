"""Classes that store logging configurations and compile into a dict for `logging.config.dictConfig()`."""

import typing as t
from dataclasses import dataclass, field

from red_utils.std.logging_utils.config_classes.base import (
    BaseHandlerConfig,
    BaseLoggingConfig,
)
from red_utils.std.logging_utils.config_classes.formatters import FormatterConfig
from red_utils.std.logging_utils.config_classes.loggers import LoggerConfig
from red_utils.std.logging_utils.config_classes.handlers import (
    FileHandlerConfig,
    QueueHandlerConfig,
    SocketHandlerConfig,
    StreamHandlerConfig,
    RotatingFileHandlerConfig,
    TimedRotatingFileHandlerConfig,
    SMTPHandlerConfig,
    QueueListenerConfig,
)


@dataclass
class LoggingConfig:
    """Assemble a logging configdict from input handlers, formatters, and loggers.

    Params:
        version (int): The logging module version. This should be `1` until the stdlib `logging` module's version changes.
        disable_existing_loggers (bool): When `True`, disable all loggers before applying logging configuration.
        formatters (dict): A dict describing formatters for the logging config.
        handlers (dict): A dict describing handlers for the logging config.
        loggers (dict): A dict describing loggers for the logging config.
    """

    version: int = 1
    disable_existing_loggers: bool = False
    propagate: bool = True
    # root: dict = field(default_factory=dict)
    formatters: dict = field(default_factory=dict)
    handlers: dict = field(default_factory=dict)
    loggers: dict = field(default_factory=dict)

    def add_formatters(self, formatter_configs: list[FormatterConfig]):
        """Append a logg"""
        for formatter in formatter_configs:
            self.formatters.update(formatter.get_configdict())

    def add_handlers(self, handler_configs: list[BaseHandlerConfig]):
        for handler in handler_configs:
            self.handlers.update(handler.get_configdict())

    def add_loggers(self, logger_configs: list[LoggerConfig]):
        for logger in logger_configs:
            self.loggers.update(logger.get_configdict())

    def get_config(self) -> dict:
        """Return a configDict initialized from the class's parameters."""
        config_dict: dict = {
            "version": self.version,
            "disable_existing_loggers": self.disable_existing_loggers,
            "propagate": self.propagate,
            "formatters": self.formatters,
            "handlers": self.handlers,
            "loggers": self.loggers,
        }

        return config_dict
