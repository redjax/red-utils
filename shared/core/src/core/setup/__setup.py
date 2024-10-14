from __future__ import annotations

import logging

log = logging.getLogger(__name__)


def setup_logging(
    level: str = "INFO",
    format: str = "%(asctime)s | [%(levelname)s] | (%(name)s) > %(module)s.%(funcName)s:%(lineno)s |> %(message)s",
    datefmt: str = "%Y-%m-%d_%H-%M-%S",
    silence_loggers: list[str] = [
        "httpx",
        "hishel",
        "httpcore",
        "urllib3",
        "sqlalchemy",
    ],
):
    logging.basicConfig(level=level, format=format, datefmt=datefmt)

    if silence_loggers:
        for _logger in silence_loggers:
            logging.getLogger(_logger).setLevel("WARNING")
