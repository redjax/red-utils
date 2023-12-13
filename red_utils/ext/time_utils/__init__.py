import pkgutil

if pkgutil.find_loader("arrow"):
    from . import arrow_utils

if pkgutil.find_loader("pendulum"):
    from . import pendulum_utils
    from .pendulum_utils import get_ts
    from .pendulum_utils.validators import validate_time_period
    from .pendulum_utils.constants import (
        TIME_FMT_24H,
        TIME_FMT_12H,
        DEFAULT_TZ,
        TS_STR_REPLACE_MAP,
        VALID_TIME_PERIODS,
    )
