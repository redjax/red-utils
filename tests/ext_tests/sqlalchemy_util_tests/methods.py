from __future__ import annotations

import random
from typing import Type

from .base import TEST_BASE
from .models import EX_TESTUSERMODEL_FULL, EX_TESTUSERMODEL_LIST, TestUserModel
from .repository import TestUserRepository
from .schemas import TestUser, TestUserOut

from loguru import logger as log
from red_utils.ext import sqlalchemy_utils
import sqlalchemy.orm as so


def init_test_db(
    base: so.DeclarativeBase = TEST_BASE,
    db_settings: sqlalchemy_utils.DBSettings = None,
    insert_models: list[TestUserModel] = EX_TESTUSERMODEL_LIST,
) -> None:
    log.info("Initializing test database")
    try:
        base.metadata.create_all(bind=db_settings.get_engine())
    except Exception as exc:
        msg = Exception(f"Unhandled exception initializing database. Details: {exc}")
        log.error(msg)

        raise exc

    # session: so.sessionmaker[so.Session] = db_settings.get_session_pool()
    session_pool: so.sessionmaker[so.Session] = sqlalchemy_utils.get_session_pool(
        engine=db_settings.get_engine(), autoflush=True
    )

    with session_pool() as session:
        repo: TestUserRepository = TestUserRepository(session=session)

        log.info(f"Inserting [{len(insert_models)}] TestUserModel(s) into the database")
        for model in insert_models:
            try:
                repo.add(entity=model)
            except Exception as exc:
                msg = Exception(
                    f"Unhandled exception inserting TestUserModel into database. TestUserModel object: {model}. Details: {exc}"
                )
                log.error(msg)


def insert_one_testuser(
    db_settings: sqlalchemy_utils.DBSettings = None,
    sqla_usermodel: TestUserModel = None,
):
    # assert session_pool is not None, ValueError("session_pool cannot be None")
    assert db_settings, ValueError("Missing DBSettings object.")
    assert sqla_usermodel is not None, ValueError("sqla_usermodel cannot be None")

    log.info(f"Inserting TestUserModel: ({sqla_usermodel.__repr__()})")
    session_pool: so.sessionmaker[so.Session] = sqlalchemy_utils.get_session_pool(
        engine=db_settings.get_engine(), autoflush=True
    )

    with session_pool() as session:
        repo = TestUserRepository(session=session())
        try:
            repo.add(sqla_usermodel)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception inserting TestUserModel into database. Model: {sqla_usermodel.__dict__}. Details: {exc}"
            )
            log.error(msg)


def get_user_schema() -> TestUser:
    user: TestUser = TestUser(
        username="TestUser1",
        email="test@example.com",
        description="This is a generic, complete TestUser schema for Pytest.",
    )

    return user


def get_list_user_schemas() -> list[TestUser]:
    users: list[TestUser] = [
        TestUser(
            username="TestListUser1", description="A TestUser in a list for Pytest"
        ),
        TestUser(
            username="TestListUser2",
            email="test2@example.com",
            description="A second TestUser in a list for Pytest",
        ),
        TestUser(
            username="TestListUser3",
            email="test3@example.com",
            description="A third TestUser in a list for Pytest",
        ),
    ]

    return users
