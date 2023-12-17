from __future__ import annotations

from red_utils.ext import time_utils
from red_utils.ext.time_utils import arrow_utils

import arrow
import pendulum

from pytest import fixture

@fixture
def bad_ts_str() -> str:
    return "20023-12-17"


@fixture
def ts_str() -> str:
    return "2023-12-17 00:00:00"


@fixture
def arrow_epoch_date() -> arrow.Arrow:
    return arrow.get("1970-01-01T00:00:00Z")


@fixture
def pendulum_epoch_date() -> pendulum.DateTime:
    return pendulum.parse("1970-01-01T:00:00:00Z")


@fixture
def arrow_now() -> arrow.Arrow:
    return arrow.now()


@fixture
def pendulum_now() -> pendulum.DateTime:
    return pendulum.now()
