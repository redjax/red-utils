import logging

log = logging.getLogger(__name__)

from core import setup
import std_time_utils as time_utils


if __name__ == "__main__":
    setup.setup_logging(level="DEBUG")
    log.info("Start demo")
    log.debug("Test DEBUG message")

    ts = time_utils.get_ts()
    log.info(f"Timestamp ({type(ts)}): {ts}")

    ts_str = time_utils.get_ts(as_str=True)
