from __future__ import annotations

from red_utils.ext import sqlalchemy_utils

from pytest import fixture
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept


@fixture
def sqla_db_settings() -> sqlalchemy_utils.DBSettings:
    db_settings: sqlalchemy_utils.DBSettings = sqlalchemy_utils.DBSettings(
        database=":memory:", echo=True
    )

    return db_settings
