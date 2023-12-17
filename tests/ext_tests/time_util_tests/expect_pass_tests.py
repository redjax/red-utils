from __future__ import annotations

from red_utils.ext import time_utils
from red_utils.ext.time_utils import arrow_utils

import arrow
import pendulum

from pytest import mark, xfail

@mark.time_utils
def test_arrow_ts_str(ts_str: str):
    assert ts_str is not None, "ts_str must not be None"
    assert isinstance(ts_str, str), f"ts_str must be of type str, not ({type(ts_str)})"

    _ts = arrow.get(ts_str)
    assert isinstance(_ts, arrow.Arrow), "_ts must be of type Arrow"


@mark.time_utils
def test_arrow_shift(arrow_now: arrow.Arrow):
    assert isinstance(arrow_now, arrow.Arrow), "arrow_now must be of type arrow.Arrow"

    shifted = arrow_now.shift(weekday=1)

    assert (
        arrow_now < shifted
    ), f"arrow_now ({arrow_now}) must be earlier than date ({shifted})"


@mark.time_utils
def test_pendulum_ts(pendulum_now):
    assert pendulum_now is not None, "ts_str must not be None"
    assert isinstance(
        pendulum_now, pendulum.DateTime
    ), f"pendulum_now must be of type pendulum.DateTime, not {type(pendulum_now)}"
