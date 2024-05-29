import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class BaseLoggingConfig(ABC):
    """Abstract base class for a full logging config dict."""

    @abstractmethod
    def get_configdict(self) -> None:
        pass


@dataclass
class BaseHandlerConfig(BaseLoggingConfig):
    """Abstract base class for a logging handler dict."""

    name: str = None
    level: str = "NOTSET"
    formatter: str = None
    filters: list | None = field(default=None)

    @abstractmethod
    def get_configdict(self) -> None:
        handler_dict: dict[str, dict[str, t.Any]] = {
            self.name: {
                "class": self.get_handler_class(),
                "level": self.level,
                "formatter": self.formatter,
            }
        }
        if self.filters:
            handler_dict[self.name]["filters"] = self.filters
        return handler_dict

    def get_handler_class(self) -> str:
        raise NotImplementedError("Subclasses must implement get_handler_class method")
