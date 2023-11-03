from __future__ import annotations

import sys

from .constants import default_color_fmt, default_fmt, default_log_dir

from typing import TextIO, Union, Generic, TypeVar
from dataclasses import dataclass, field

## Generic type for dataclass classes
T = TypeVar("T")


@dataclass
class DictMixin:
    """Mixin class to add "as_dict()" method to classes. Equivalent to .__dict__.

    Add a .as_dict() method to classes that inherit from this mixin. For example,
    to add .as_dict() method to a parent class, where all children inherit the .as_dict()
    function, declare parent as:

    @dataclass
    class Parent(DictMixin):
        ...

    and call like:

        p = Parent()
        p_dict = p.as_dict()
    """

    def as_dict(self: Generic[T]):
        """Return dict representation of a dataclass instance."""
        try:
            return self.__dict__.copy()

        except Exception as exc:
            raise Exception(
                f"Unhandled exception converting class instance to dict. Details: {exc}"
            )


@dataclass
class LoguruSinkBase(DictMixin):
    """Base Loguru sink class.

    Define common options for children to inherit from.
    """

    sink: Union[str, TextIO] = field(default=sys.stdout)
    format: str = field(default=default_fmt)
    level: str = field(default="INFO")
    colorize: bool = field(default=False)

    def __post_init__(self):
        self.level = self.level.upper()


@dataclass
class LoguruSinkDefault(LoguruSinkBase):
    """Default Loguru sink. Defaults to colorized, formatted stdout, level=INFO.

    Use this class as a starting point to create customized Loguru sinks. Create a new class
    by inheriting from this one:

    my_loguru_sink = LoguruSinkDefault(sink=...,level=..., colorize=True)
    """

    pass


@dataclass
class LoguruSinkStdOut(LoguruSinkBase, DictMixin):
    format: str = field(default=default_color_fmt)
    colorize: bool = field(default=True)


@dataclass
class LoguruSinkStdErr(LoguruSinkBase):
    sink: Union[str, TextIO] = field(default=sys.stderr)
    format: str = field(default=default_color_fmt)
    colorize: bool = field(default=True)


@dataclass
class LoguruSinkFileBase(DictMixin):
    """Base class for file sinks."""

    sink: Union[str, TextIO] = field(default=f"{default_log_dir}/app.log")
    colorize: bool = field(default=True)
    retention: Union[str, int] = field(default=3)
    rotation: str = field(default="5 MB")
    format: str = field(default=default_fmt)
    level: str = field(default="DEBUG")
    enqueue: bool = field(default=True)


@dataclass
class LoguruSinkFileDefault(LoguruSinkFileBase):
    """Default Loguru file sink. Defaults to app.log, level=DEBUG.

    Use this class as a starting point to create customized Loguru file sinks. Create a new class
    by inheriting from this one:

    my_loguru_file_sink = LoguruSinkFileDefault(sink=...,level=..., colorize=True)
    """

    pass


@dataclass
class LoguruSinkAppFile(LoguruSinkFileBase, DictMixin):
    """Sink class for app.log file."""

    pass


@dataclass
class LoguruSinkErrFile(LoguruSinkFileBase):
    """Sink class for error.log file."""

    sink: Union[str, TextIO] = field(default=f"{default_log_dir}/error.log")
    level: str = field(default="ERROR")


@dataclass
class LoguruSinkTraceFile(LoguruSinkFileBase):
    """Sink class for trace.log file."""

    sink: Union[str, TextIO] = field(default=f"{default_log_dir}/trace.log")
    level: str = field(default="TRACE")
    filter: str = field(default="TRACE")
    backtrace: bool = field(default=True)
    diagnose: bool = field(default=True)


## stderr, no color
default_stderr_sink: dict = {
    "sink": sys.stderr,
    "colorize": False,
    "format": default_fmt,
    "level": "DEBUG",
}

## stderr, colorized
default_stderr_color_sink: dict = {
    "sink": sys.stderr,
    "colorize": True,
    "format": default_color_fmt,
    "level": "DEBUG",
}

## stdout, no color
default_stdout_sink: dict = {
    "sink": sys.stdout,
    "colorize": False,
    "format": default_fmt,
    "level": "DEBUG",
}

## stdout, colorized
default_stdout_color_sink: dict = {
    "sink": sys.stdout,
    "colorize": True,
    "format": default_color_fmt,
    "level": "DEBUG",
}

## logs/app.log file
default_app_log_file_sink: dict = {
    "sink": f"{default_log_dir}/app.log",
    "colorize": True,
    "retention": 3,
    "rotation": "5 MB",
    "format": default_fmt,
    "level": "DEBUG",
    "enqueue": True,
}

## logs/error.log file
default_error_log_file_sink: dict = {
    "sink": f"{default_log_dir}/error.log",
    "colorize": True,
    "retention": 3,
    "rotation": "5 MB",
    "format": default_fmt,
    "level": "ERROR",
    "enqueue": True,
}

## logs/trace.log file
default_trace_log_file_sink: dict = {
    "sink": f"{default_log_dir}/trace.log",
    "colorize": True,
    "retention": 3,
    "rotation": "5MB",
    "format": default_fmt,
    "level": "TRACE",
    "filter": "TRACE",
    "backtrace": True,
    "diagnose": True,
    "enqueue": True,
}


default_sinks: list[dict] = [
    default_stderr_color_sink,
    default_app_log_file_sink,
    default_error_log_file_sink,
    default_trace_log_file_sink,
]
