from __future__ import annotations

import random

from .base import TEST_BASE
from .methods import (
    create_base_metadata,
    get_list_user_schemas,
    get_user_schema,
    initialize_test_db,
    insert_testusermodel,
)
from .models import EX_TESTUSERMODEL_FULL, EX_TESTUSERMODEL_LIST, TestUserModel
from .schemas import TestUser, TestUserOut

from loguru import logger as log
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
def test_fail_sqla_create_base_metadata(
    sqla_base: so.DeclarativeBase = TEST_BASE, sqla_engine: sa.Engine = None
):
    create_base_metadata(sqla_base=sqla_base, sqla_engine=sqla_engine)


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


@mark.xfail
@mark.sqla_utils
def test_fail_sqla_insert_user(
    sqla_sqlite_engine: sa.Engine,
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodel=EX_TESTUSERMODEL_FULL,
):
    try:
        initialize_test_db(
            engine=sqla_sqlite_engine, base=sqla_base, insert_models=sqla_usermodel
        )

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception inserting TestUserModel into database. Details: {exc}"
        )
        log.error(msg)

        raise msg


@mark.xfail
@mark.sqla_utils
def test_fail_sqla_select_all_users(
    sqla_session: so.sessionmaker[so.Session],
    sqla_sqlite_engine: so.sessionmaker[so.Session],
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: list[TestUserModel] = EX_TESTUSERMODEL_FULL,
):
    ## Don't initialize DB, forcing test to fail
    # initialize_test_db(
    #     engine=sqla_sqlite_engine, base=sqla_base, insert_models=[sqla_usermodels]
    # )

    with sqla_session() as session:
        users = session.query(TestUserModel).all()
        log.info(f"All TestUserModels in database ({type(users)}): {users}")

        for user in users:
            log.info(f"SELECT TestUserModel ({type(user)}): {user}")

            try:
                user_schema: TestUserOut = TestUserOut.model_validate(user.__dict__)
                log.info(f"SELECT TestUserOut: {user_schema}")
            except Exception as exc:
                raise Exception(
                    f"Unhandled exception converting TestUserModel to TestUserOut schema. Details: {exc}"
                )


@mark.xfail
@mark.sqla_utils
def test_delete_user(
    sqla_session: so.sessionmaker[so.Session],
    sqla_sqlite_engine: so.sessionmaker[so.Session],
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: TestUserModel = EX_TESTUSERMODEL_LIST,
):
    initialize_test_db(
        engine=sqla_sqlite_engine, base=sqla_base, insert_models=sqla_usermodels
    )

    with sqla_session() as session:
        try:
            usermodels: list[TestUserModel] = session.query(TestUserModel).all()
        except Exception as exc:
            raise Exception(
                f"Unhandled exception selecting TestUserModel from database. Details: {exc}"
            )

        rand_index = random.randint(0, len(usermodels) - 1)
        usermodel: TestUserModel = usermodels[rand_index]
        log.info(f"SELECT TestUserModel: {usermodel.__dict__}")

        userschema: TestUserOut = TestUserOut.model_validate(usermodel)
        log.info(f"Deleting User: {userschema}")

        try:
            ## Set usermodel to None to force test to fail
            usermodel = None
            session.delete(usermodel)
            log.success(f"Deleted TestUserModel with ID [{usermodel.user_id}]")
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception deleting TestUserModel with ID [{usermodel.user_id}]. Test User: {userschema}. Details: {exc}"
            )
            log.error(msg)

            raise msg

        session.commit()
