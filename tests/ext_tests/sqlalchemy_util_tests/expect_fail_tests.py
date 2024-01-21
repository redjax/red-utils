from __future__ import annotations

from pytest import mark, xfail
from red_utils.ext import sqlalchemy_utils
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

@mark.xfail
@mark.sqla_utils
def test_fail_sqla_base(sqla_base: so.DeclarativeBase):
    assert sqla_base is not None, ValueError("Missing sqla_base")
    assert isinstance(sqla_base, so.DeclarativeBase), TypeError(
        f"Expected failure, sqla_base is not of type DeclarativeAttributeIntercept. Type: ({type(sqla_base)})"
    )


@mark.xfail
@mark.sqla_utils
def test_fail_sqla_sqlite_in_memory_conn(
    sqla_sqlite_inmemory: sqlalchemy_utils.saSQLiteConnection,
):
    assert sqla_sqlite_inmemory is not None, ValueError(
        "sqla_sqlite_inmemory cannot be None"
    )
    assert not isinstance(
        sqla_sqlite_inmemory, sqlalchemy_utils.saSQLiteConnection
    ), TypeError(
        f"sqla_sqlite_inmemory must be of type saSQLiteConnection, not ({type(sqla_sqlite_inmemory)})"
    )


@mark.xfail
@mark.sqla_utils
def test_fail_sqla_sqlite_engine(sqla_sqlite_engine: sa.Engine):
    assert sqla_sqlite_engine is not None, ValueError(
        "sqla_sqlite_engine cannot be None"
    )
    assert not isinstance(sqla_sqlite_engine, sa.Engine), TypeError(
        f"sqla_sqlite_engine must be of type sqlalchemy.Engine. Got type: ({type(sqla_sqlite_engine)})"
    )
