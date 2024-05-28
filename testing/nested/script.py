from loguru import logger as log


def test_logs():
    log.debug(f"Log from {__name__}")
    log.info(f"Log from {__name__}")
