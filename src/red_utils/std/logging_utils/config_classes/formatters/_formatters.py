from dataclasses import dataclass

from red_utils.std.logging_utils.config_classes.base import BaseLoggingConfig
from red_utils.std.logging_utils.fmts._formats import (
    MESSAGE_FMT_BASIC,
    MESSAGE_FMT_DETAILED,
    MESSAGE_FMT_STANDARD,
    RED_UTILS_DETAIL_FMT,
    RED_UTILS_FMT,
    DATE_FMT_DATE_ONLY,
    DATE_FMT_STANDARD,
    DATE_FMT_TIME_ONLY,
)


@dataclass
class FormatterConfig(BaseLoggingConfig):
    """Define a logging formatter."""

    name: str = None
    fmt: str = MESSAGE_FMT_STANDARD
    datefmt: str = DATE_FMT_STANDARD
    style: str = "%"
    validate: bool = True

    def get_configdict(self) -> dict[str, dict[str, str]]:
        formatter_dict: dict[str, dict[str, str]] = {self.name: {"format": self.fmt}}
        if self.datefmt:
            formatter_dict[self.name]["datefmt"] = self.datefmt
        if self.style:
            formatter_dict[self.name]["style"] = self.style
        formatter_dict[self.name]["validate"] = self.validate

        return formatter_dict
