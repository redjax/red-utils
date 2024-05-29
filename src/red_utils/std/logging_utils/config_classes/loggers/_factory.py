import logging
import logging.config


class LoggerFactory:
    _LOG: logging.Logger | None = None

    @staticmethod
    def __create_logger(
        name: str,
        log_level: str,
        handlers: dict[str, dict],
        formatters: dict[str, dict],
        loggers: dict[str, dict],
    ) -> logging.Logger:
        """Internal class method to handle creating a logger."""
        log_level = log_level.upper()

        # Configure logging using dictConfig
        logging_config = {
            "version": 1,
            "handlers": handlers,
            "formatters": formatters,
            "loggers": loggers,
            "root": {
                "level": log_level,
                "handlers": list(handlers.keys()),
            },
        }

        try:
            logging.config.dictConfig(logging_config)
        except Exception as exc:
            msg = Exception(f"Unhandled exception configuring logger. Details: {exc}")
            # log.error(msg)

            raise msg

        # Get or create logger
        LoggerFactory._LOG = logging.getLogger(name)

        return LoggerFactory._LOG

    @staticmethod
    def get_logger(
        name: str,
        log_level: str,
        handlers: dict[str, dict],
        formatters: dict[str, dict],
        loggers: dict[str, dict],
    ) -> logging.Logger:
        """Initialize a logger."""
        logger = LoggerFactory.__create_logger(
            name=name,
            log_level=log_level,
            handlers=handlers,
            formatters=formatters,
            loggers=loggers,
        )

        return logger
