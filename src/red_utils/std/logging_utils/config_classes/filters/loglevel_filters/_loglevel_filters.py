import logging


def debug_filter(record: logging.LogRecord) -> bool:
    """Filter to only show DEBUG and above."""
    return record.levelno >= logging.DEBUG


def info_filter(record: logging.LogRecord) -> bool:
    """Filter to only show INFO and above."""
    return record.levelno >= logging.INFO


def warning_filter(record: logging.LogRecord) -> bool:
    """Filter to only show WARNING and above."""
    return record.levelno >= logging.WARNING


def error_filter(record: logging.LogRecord) -> bool:
    """Filter to only show ERROR and above."""
    return record.levelno >= logging.ERROR


def critical_filter(record: logging.LogRecord) -> bool:
    """Filter to only show CRITICAL and above."""
    return record.levelno >= logging.CRITICAL
