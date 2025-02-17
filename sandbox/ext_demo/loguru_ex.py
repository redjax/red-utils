# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "loguru",
#     "red-utils",
# ]
#
# [tool.uv.sources]
# red-utils = { path = "../../" }
# ///
from __future__ import annotations

from red_utils.ext import loguru_utils

from loguru import logger as log

if __name__ == "__main__":
    loguru_utils.init_logger(sinks=[loguru_utils.sinks.default_stderr_sink])
    log.info("Test")
    log.debug("Test")
