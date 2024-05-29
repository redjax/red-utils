import typing as t
from dataclasses import dataclass

from red_utils.std.logging_utils.config_classes.base import BaseLoggingConfig


@dataclass
class LoggerConfig(BaseLoggingConfig):
    name: str
    level: str
    handlers: list[str]
    propagate: bool = False

    def get_configdict(self) -> dict:
        logger_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "level": self.level,
                "handlers": self.handlers,
                "propagate": self.propagate,
            }
        }
        return logger_dict
