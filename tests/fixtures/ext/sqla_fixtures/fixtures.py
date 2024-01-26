from __future__ import annotations

from pytest import fixture
from red_utils.ext import sqlalchemy_utils
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

@fixture
def sqla_sqlite_inmemory() -> sqlalchemy_utils.saSQLiteConnection:
    conn: sqlalchemy_utils.saSQLiteConnection = sqlalchemy_utils.saSQLiteConnection(
        database=":memory:"
    )

    assert conn is not None, ValueError("sqla_sqlite_inmemory cannot be None")
    assert isinstance(conn, sqlalchemy_utils.saSQLiteConnection), TypeError(
        f"sqla_sqlite_inmemory must be of type saSQLiteConnection, not ({type(sqla_sqlite_inmemory)})"
    )

    return conn


@fixture
def sqla_sqlite_engine(
    sqla_sqlite_inmemory: sqlalchemy_utils.saSQLiteConnection,
) -> sa.Engine:
    assert sqla_sqlite_inmemory is not None, ValueError(
        "sqla_sqlite_inmemory fixture cannot be None, expected an instance of sqlalchemy_utils.saSQLiteConnection"
    )
    assert isinstance(
        sqla_sqlite_inmemory, sqlalchemy_utils.saSQLiteConnection
    ), TypeError(
        f"sqla_sqlite_inmemory fixture must be of type sqlalchemy_utils.saSQLiteConnection. Got type: ({type(sqla_sqlite_inmemory)})"
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


@fixture
def sqla_session(sqla_sqlite_engine: sa.Engine):
    assert sqla_sqlite_engine is not None, ValueError(
        "sqla_sqlite_engine fixture cannot be None"
    )
    assert isinstance(sqla_sqlite_engine, sa.Engine), TypeError(
        f"sqla_sqlite_engine fixture must be of type sqlalchemy.Engine. Got type: ({type(sqla_sqlite_engine)})"
    )

    try:
        session_pool: so.sessionmaker[so.Session] = so.sessionmaker(
            bind=sqla_sqlite_engine
        )
        assert session_pool is not None, ValueError(
            "session_pool should not have been None"
        )
        assert isinstance(session_pool, so.sessionmaker), TypeError(
            f"session_pool should have been of type sqlalchemy.orm.sessionmaker. Got type: ({type(session_pool)})"
        )

        return session_pool
    except Exception as exc:
        raise Exception(
            f"Unhandled exception initializing SQLAlchemy Session pool fixture. Details: {exc}"
        )
