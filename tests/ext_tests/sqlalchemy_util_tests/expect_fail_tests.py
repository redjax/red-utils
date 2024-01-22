from __future__ import annotations

from .base import TEST_BASE
from .models import TestUserModel

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
def test_fail_sqla_create_base_metadata(sqla_base: so.DeclarativeBase = TEST_BASE):
    sqla_base.metadata.create_all(bind=None)


@mark.xfail
@mark.sqla_utils
def test_fail_sqla_sqlite_session_pool(sqla_session: so.sessionmaker[so.Session]):
    with sqla_session() as session:
        session.execute(sa.text("SELECT * FROM nonexistant"))


@mark.xfail
@mark.sqla_utils
def test_fail_sqla_create_usermodel():
    sqla_fail_usermodel: TestUserModel = TestUserModel()
    assert sqla_fail_usermodel.username is not None, ValueError(
        "Expected failure, TestUser.username is null"
    )
