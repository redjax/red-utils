from _collections_abc import dict_keys
import random
from typing import Type

from .base import TEST_BASE
from .methods import (
    init_test_db,
    get_list_user_schemas,
    get_user_schema,
)
from .models import EX_TESTUSERMODEL_FULL, EX_TESTUSERMODEL_LIST, TestUserModel
from .schemas import TestUser, TestUserOut, TestUserUpdate
from .repository import TestUserRepository

from loguru import logger as log
from pytest import mark, xfail
from red_utils.ext import sqlalchemy_utils
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger
from regex import E
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

init_logger([LoguruSinkStdOut(level="DEBUG").as_dict()])


@mark.sqla_utils
def test_user_schema():
    user: TestUser = get_user_schema()

    assert user, ValueError("TestUser should not have been None")
    assert isinstance(user, TestUser), TypeError(
        f"user should have been a TestUser object. Got type: ({type(user)})"
    )

    log.success(f"TestUser schema: {user}")


@mark.sqla_utils
def test_convert_user_schema_to_model() -> None:
    user: TestUser = get_user_schema()

    try:
        user_model: TestUserModel = TestUserModel(
            username=user.username, email=user.email, description=user.description
        )
        log.success(
            f"TestUser schema converted to TestUserModel.\n\tSchema: {user}\n\tModel: {user_model.__repr__()}"
        )

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception converting TestUser schema to TestUserModel. Detail: {exc}"
        )
        log.error(msg)

        raise msg


@mark.sqla_utils
def test_sqla_create_base_metadata(
    sqla_db_settings: sqlalchemy_utils.DBSettings,
    sqla_base: so.DeclarativeBase = TEST_BASE,
) -> None:
    try:
        sqlalchemy_utils.create_base_metadata(
            engine=sqla_db_settings.get_engine(), base_obj=sqla_base
        )
    except Exception as exc:
        msg = Exception(
            f"Unhandled exception creating test Base metadata. Details: {exc}"
        )
        log.error(msg)

        raise msg


@mark.sqla_utils
def test_sqla_list_tables(
    sqla_db_settings: sqlalchemy_utils.DBSettings,
    sqla_base: so.DeclarativeBase = TEST_BASE,
) -> None:
    try:
        sqlalchemy_utils.create_base_metadata(
            engine=sqla_db_settings.get_engine(), base_obj=sqla_base
        )
        tables: dict_keys[str, sa.Table] = sqla_base.metadata.tables.keys()

        log.info(f"Database tables: {tables}")

    except Exception as exc:
        msg = Exception(
            f"Unhandled exception creating Base table metadata. Details: {exc}"
        )
        log.error(msg)

        raise msg


@mark.sqla_utils
def test_sqla_sqlite_session_pool(
    sqla_db_settings: sqlalchemy_utils.DBSettings = sqlalchemy_utils.DBSettings,
):
    assert sqla_db_settings, ValueError("Missing DBSettings object")
    # assert isinstance(sqla_db_settings, sqlalchemy_utils.DBSettings), TypeError(
    #     f"sqla_db_settings should be a DBSettings object. Got type: ({type(sqla_db_settings)})"
    # )

    session_pool: so.sessionmaker[so.Session] = sqlalchemy_utils.get_session_pool(
        engine=sqla_db_settings.get_engine(), autoflush=True
    )

    with session_pool() as session:
        session.execute(sa.text("SELECT 1"))


@mark.sqla_utils
def test_sqla_create_usermodel(sqla_usermodel: TestUserModel = EX_TESTUSERMODEL_FULL):
    sqla_usermodel: TestUserModel = TestUserModel(
        username="TestUser1",
        email="test@example.com",
        description="This is a TestUserModel instance created for use in Pytest.",
    )
    log.info(f"TestUserModel: {sqla_usermodel.__repr__()}")

    usermodel_schema: TestUser = TestUser.model_validate(sqla_usermodel.__dict__)
    log.info(f"TestUser schema: {usermodel_schema}")


@mark.sqla_utils
def test_sqla_insert_user(
    sqla_db_settings: sqlalchemy_utils.DBSettings,
    sqla_usermodel=EX_TESTUSERMODEL_FULL,
):
    session_pool: so.sessionmaker[so.Session] = sqlalchemy_utils.get_session_pool(
        engine=sqla_db_settings.get_engine(), autoflush=True
    )

    with session_pool() as session:
        repo = TestUserRepository(session=session)
        try:
            repo.add(sqla_usermodel)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception inserting TestUserModel into database. TestUserModel: {sqla_usermodel}. Details: {exc}"
            )
            log.error(msg)

            raise msg


@mark.sqla_utils
def test_sqla_select_all_users(
    sqla_db_settings: sqlalchemy_utils.DBSettings,
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: list[TestUserModel] = EX_TESTUSERMODEL_FULL,
):
    init_test_db(
        db_settings=sqla_db_settings, base=sqla_base, insert_models=[sqla_usermodels]
    )

    session_pool: so.sessionmaker[so.Session] = sqlalchemy_utils.get_session_pool(
        engine=sqla_db_settings.get_engine(), autoflush=True
    )

    with session_pool() as session:
        repo = TestUserRepository(session=session)

        users: list[TestUserModel] = repo.get_all()
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


@mark.sqla_utils
def test_delete_user(
    sqla_db_settings: sqlalchemy_utils.DBSettings,
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: TestUserModel = EX_TESTUSERMODEL_LIST,
):
    init_test_db(
        db_settings=sqla_db_settings, base=sqla_base, insert_models=[sqla_usermodels]
    )

    session_pool: so.sessionmaker[so.Session] = sqlalchemy_utils.get_session_pool(
        engine=sqla_db_settings.get_engine(), autoflush=True
    )

    with session_pool() as session:
        repo = TestUserRepository(session=session())

        try:
            usermodels: list[TestUserModel] = repo.get_all()
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
            repo.remove(usermodel)
            log.success(f"Deleted TestUserModel with ID [{usermodel.user_id}]")
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception deleting TestUserModel with ID [{usermodel.user_id}]. Test User: {userschema}. Details: {exc}"
            )
            log.error(msg)

            raise msg


def test_update_user(
    sqla_db_settings: sqlalchemy_utils.DBSettings,
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: TestUserModel = EX_TESTUSERMODEL_LIST,
):
    init_test_db(
        db_settings=sqla_db_settings, base=sqla_base, insert_models=[sqla_usermodels]
    )

    session_pool: so.sessionmaker[so.Session] = sqlalchemy_utils.get_session_pool(
        engine=sqla_db_settings.get_engine(), autoflush=True
    )

    with session_pool() as session:
        repo = TestUserRepository(session=session())

        usermodels: list[TestUserModel] = repo.get_all()

        assert usermodels is not None, ValueError(
            "usermodels should not have been None"
        )
        assert isinstance(usermodels, list), TypeError(
            f"usermodels should have been a non-empty list."
        )
        assert len(usermodels) > 0, ValueError("usermodels list cannot be empty")

        rand_index: int = random.randint(0, len(usermodels) - 1)
        usermodel: TestUserModel = usermodels[rand_index]

        log.info(f"SELECT TestUserModel: {usermodel.__dict__}")
