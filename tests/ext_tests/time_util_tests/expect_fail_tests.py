from __future__ import annotations

from red_utils.ext import time_utils
from red_utils.ext.time_utils import arrow_utils

import arrow
import pendulum
from pytest import mark, xfail

@mark.xfail
def test_fail_arrow_ts(bad_ts_str: str):
    assert bad_ts_str is not None, "bad_ts_str must not be None"
    assert isinstance(
        bad_ts_str, str
    ), f"bad_ts_str must be of type str, not {type(bad_ts_str)}"

    bad_ts = arrow.get(bad_ts_str)

    assert isinstance(
        bad_ts, arrow.Arrow
    ), f"bad_ts must be of type arrow.Arrow, not ({type(bad_ts)})"


@mark.xfail
def test_fail_arrow_shift():
    ts = arrow.now()
    assert isinstance(ts, arrow.Arrow), "ts must be of type arrow.Arrow"

    shifted = ts.shift(weekday=1)

    assert ts > shifted, f"ts ({ts}) must be later than date ({shifted})"


@mark.xfail
def test_fail_pendulum_ts(bad_ts_str: str):
    assert bad_ts_str is not None, "bad_ts_str must not be None"
    assert isinstance(
        bad_ts_str, str
    ), f"bad_ts_str must be of type str, not {type(bad_ts_str)}"

    bad_ts = pendulum.parse(bad_ts_str)

    assert isinstance(
        bad_ts, pendulum.DateTime
    ), f"bad_ts must be of type pendulum.DateTime, not ({type(bad_ts)})"


@mark.xfail
def test_fail_pendulum_24h_ts():
    time_utils.get_ts(as_str=True, str_fmt=1)


@mark.xfail
def test_fail_pendulum_char_replace():
    ts = time_utils.get_ts(
        as_str=True, safe_str=True, char_replace_map=[{"search": "-", "replace": "^"}]
    )
    assert ts is not None, "ts must not be None"
    assert isinstance(ts, str), f"ts must be of type str, not ({type(ts)})"
    assert (
        "^" not in ts
    ), f"Timestamp missing expected '^' character. Timestamp string: {ts}"
