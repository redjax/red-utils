"""Pre-built formats that can be imported and set as a logger/handler's `format` and `datefmt` params."""

from __future__ import annotations

RED_UTILS_FMT: str = str(
    "[%(asctime)s] [%(levelname)s] [(red_utils).%(module)s:%(lineno)d > %(funcName)s()]: %(message)s"
)
RED_UTILS_DETAIL_FMT: str = str(
    "[%(asctime)s] [%(levelname)s] [(red_utils).%(module)s] [path:%(pathname)s:%(lineno)d] [method:%(funcName)s()]: %(message)s"
)

MESSAGE_FMT_STANDARD: str = str(
    "[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d > %(funcName)s()]: %(message)s"
)
MESSAGE_FMT_DETAILED: str = str(
    "[%(asctime)s] [%(levelname)s] [module:%(module)s] [path:%(pathname)s:%(lineno)d] [method:%(funcName)s()]: %(message)s"
)
MESSAGE_FMT_BASIC: str = "%(asctime)-19s %(levelname)-8s : %(message)s"
DATE_FMT_STANDARD: str = "%Y-%m-%d %H:%M:%S"
DATE_FMT_DATE_ONLY: str = "%Y-%m-%d"
DATE_FMT_TIME_ONLY: str = "%H:%M:%S"
