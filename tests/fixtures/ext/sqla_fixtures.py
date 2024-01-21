from __future__ import annotations

from pytest import fixture
from red_utils.ext import sqlalchemy_utils
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

@fixture
def sqla_base() -> DeclarativeAttributeIntercept:
    return sqlalchemy_utils.Base


@fixture
def sqla_sqlite_inmemory() -> sqlalchemy_utils.saSQLiteConnection:
    conn: sqlalchemy_utils.saSQLiteConnection = sqlalchemy_utils.saSQLiteConnection(
        database=":memory:"
    )

    return conn


@fixture
def sqla_sqlite_engine(
    sqla_sqlite_inmemory: sqlalchemy_utils.saSQLiteConnection,
) -> sa.Engine:
    assert sqla_sqlite_inmemory is not None, ValueError(
        "conn cannot be None, expected an instance of sqlalchemy_utils.saSQLiteConnection"
    )
    assert isinstance(
        sqla_sqlite_inmemory, sqlalchemy_utils.saSQLiteConnection
    ), TypeError(
        f"conn must be of type sqlalchemy_utils.saSQLiteConnection. Got type: ({type(sqla_sqlite_inmemory)})"
    )

    try:
        engine: sa.Engine = sqlalchemy_utils.get_engine(connection=sqla_sqlite_inmemory)

        assert engine is not None, ValueError("engine cannot not be None")
        assert isinstance(engine, sa.Engine), TypeError(
            f"engine must be of type sqlalchemy.Engine. Got type: ({type(engine)})"
        )

        return engine
    except Exception as exc:
        raise Exception(
            f"Unhandled exception initializing SQLAlchemy Engine fixture. Details: {exc}"
        )
