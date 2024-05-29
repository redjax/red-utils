import typing as t
from .handlers import (
    FileHandlerConfig,
    RotatingFileHandlerConfig,
    TimedRotatingFileHandlerConfig,
    StreamHandlerConfig,
    SocketHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
)

HANDLER_CLASSES_TYPE = t.Union[
    FileHandlerConfig,
    RotatingFileHandlerConfig,
    TimedRotatingFileHandlerConfig,
    StreamHandlerConfig,
    SocketHandlerConfig,
    QueueHandlerConfig,
    QueueListenerConfig,
]
HANDLER_CLASSES_TYPE_ANNOTATION = t.Annotated[
    HANDLER_CLASSES_TYPE,
    "A logging handler config class.",
]
LOGGING_CONFIG_DICT_TYPE = dict[str, dict[str, t.Any]]
LOGGING_CONFIG_DICT_TYPE_ANNOTATION = t.Annotated[
    LOGGING_CONFIG_DICT_TYPE, "A logging dictConfig-compatible dict."
]
