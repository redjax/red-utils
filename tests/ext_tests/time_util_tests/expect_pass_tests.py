from __future__ import annotations

import pendulum
from pytest import mark, xfail
from red_utils.ext import time_utils

@mark.time_utils
def test_pendulum_ts(pendulum_now):
    assert pendulum_now is not None, "ts_str must not be None"
    assert isinstance(
        pendulum_now, pendulum.DateTime
    ), f"pendulum_now must be of type pendulum.DateTime, not {type(pendulum_now)}"


@mark.time_utils
def test_pendulum_24h_ts():
    ts = time_utils.get_ts(as_str=True, str_fmt=time_utils.TIME_FMT_24H)
    assert ts is not None, "ts must not be None"
    assert isinstance(ts, str), f"ts must be of type str, not ({type(ts)})"


@mark.time_utils
def test_pendulum_get_ts():
    ts = time_utils.get_ts()
    assert ts is not None, "ts must not be None"
    assert isinstance(
        ts, pendulum.DateTime
    ), f"ts must be of type pendulum.DateTime, not ({type(ts)})"


@mark.time_utils
def test_pendulum_safestr():
    ts = time_utils.get_ts(as_str=True, safe_str=True)
    assert ts is not None, "ts must not be None"
    assert isinstance(ts, str), f"ts must be of type str, not ({type(ts)})"


@mark.time_utils
def test_pendulum_char_replace():
    ts = time_utils.get_ts(
        as_str=True, safe_str=True, char_replace_map=[{"search": "-", "replace": "^"}]
    )
    assert ts is not None, "ts must not be None"
    assert isinstance(ts, str), f"ts must be of type str, not ({type(ts)})"
    assert (
        "^" in ts
    ), f"Timestamp missing expected '^' character. Timestamp string: {ts}"
