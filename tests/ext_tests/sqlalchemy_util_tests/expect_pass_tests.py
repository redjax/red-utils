import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from pytest import mark, xfail
from red_utils.ext import sqlalchemy_utils

@mark.sqla_utils
def test_sqla_base(sqla_base: so.DeclarativeBase):
    assert sqla_base is not None, ValueError("Missing a SQLAlchemy DeclarativeBase object")
    assert isinstance(sqla_base, so.DeclarativeBase) or isinstance(sqla_base, DeclarativeAttributeIntercept), TypeError(f"sqla_base must be of type sqlalchemy.orm.DeclarativeBase, not ({type(sqla_base)})")

@mark.sqla_utils
def test_sqla_sqlite_in_memory_conn(sqla_sqlite_inmemory: sqlalchemy_utils.saSQLiteConnection):
    assert sqla_sqlite_inmemory is not None, ValueError("sqla_sqlite_inmemory cannot be None")
    assert isinstance(sqla_sqlite_inmemory, sqlalchemy_utils.saSQLiteConnection), TypeError(f"sqla_sqlite_inmemory must be of type saSQLiteConnection, not ({type(sqla_sqlite_inmemory)})")

@mark.sqla_utils
def test_sqla_sqlite_engine(sqla_sqlite_engine: sa.Engine):
    assert sqla_sqlite_engine is not None, ValueError("sqla_sqlite_engine cannot be None")
    assert isinstance(sqla_sqlite_engine, sa.Engine), TypeError(f"sqla_sqlite_engine must be of type sqlalchemy.Engine. Got type: ({type(sqla_sqlite_engine)})")
