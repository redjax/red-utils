import typing as t
import logging
import logging.config
from copy import deepcopy

log = logging.getLogger("red_utils.std.logging_utils.setup")

from red_utils.std.logging_utils._methods import merge_config_dicts


def setup_logging(
    app_name: str = "app",
    log_level: str = "DEBUG",
    merge_logging_configs: list[dict] | None = None,
):
    """Initialize Python's standard logging module.

    This method uses my personal preferred log message formats and other defaults. You may want to just reference
    the logging_config dict in this method and create your own logging setup method based on this one.
    """
    ## Logging config dict
    logging_config: dict[str, t.Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "[%(asctime)s] [%(levelname)s] [%(module)s:%(lineno)d > %(funcName)s()]: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
            "detail": {
                "format": "[%(asctime)s] [%(levelname)s] [module:%(module)s] [path:%(pathname)s:%(lineno)d] [method:%(funcName)s()]: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "standard",
                "stream": "ext://sys.stdout",
            }
        },
        "loggers": {
            "": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
            app_name: {
                "handlers": ["console"],
                "level": log_level.upper(),
                "propagate": False,
            },
            "notebook": {
                "handlers": ["console"],
                "level": "WARNING",
                "propagate": False,
            },
        },
    }

    if merge_logging_configs is not None:
        try:
            ## Make a copy of the logging config so you don't alter the original
            merged_config = deepcopy(logging_config)

            CONTINUE_MERGE: bool = True
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception copying logging configdict. Details: {exc}"
            )
            log.error(msg)

            CONTINUE_MERGE = False

        ## Initialize a variable to denote success merging config dicts
        MERGE_SUCCESS: bool = True

        ## Get maximum number of loops
        MAX_LOOPS: int = len(merge_logging_configs)
        ## Initialize loop count
        LOOP_COUNT: int = 0

        while CONTINUE_MERGE:
            if LOOP_COUNT == MAX_LOOPS:
                break
            else:
                ## Loop over config dicts
                for _configdict in merge_logging_configs:
                    try:
                        ## Merge existing config dict (which may contain merged elements)
                        merged_config = merge_config_dicts(
                            configdict1=merged_config, configdict2=_configdict
                        )

                        ## Merge success
                        CONTINUE_MERGE = True
                        LOOP_COUNT += 1

                    except Exception as exc:
                        ## Merge error
                        msg = Exception(
                            f"Unhandled exception merging dicts. Details: {exc}"
                        )
                        log.error(msg)

                        MERGE_SUCCESS = False
                        ## Break loop
                        CONTINUE_MERGE = False

                    if CONTINUE_MERGE:
                        continue
                    else:
                        log.warning(
                            "Error encountered while merging logging config dicts. Reverting to original logging_config dict."
                        )
                        # merged_config = logging_config
                        MERGE_SUCCESS = False

        if MERGE_SUCCESS:
            logging_config = merged_config
        else:
            logging_config = logging_config

    try:
        logging.config.dictConfig(logging_config)
    except Exception as exc:
        msg = Exception(f"Unhandled exception configuring logging. Details: {exc}")
        logging.error(msg)

        raise exc
