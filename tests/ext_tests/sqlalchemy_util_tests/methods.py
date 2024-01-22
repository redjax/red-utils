from __future__ import annotations

from .models import TestUserModel
from .schemas import TestUser, TestUserOut

import sqlalchemy as sa
import sqlalchemy.orm as so

def create_base_metadata(
    sqla_base: so.DeclarativeBase = None, sqla_engine: sa.Engine = None
):
    """Test method for creating SQLAlchemy Base metadata."""
    assert sqla_base is not None, ValueError("sqla_base cannot be None")
    assert sqla_engine is not None, ValueError("sqla_engine cannot be None")

    try:
        sqla_base.metadata.create_all(bind=sqla_engine)
        print(f"SQLAlchemy Base metadata created")
    except Exception as exc:
        raise Exception(
            f"Unhandled exception creating SQLAlchemy Base metadata. Details: {exc}"
        )


def insert_testusermodel(
    session_pool: so.sessionmaker[so.Session] = None,
    sqla_usermodel: TestUserModel = None,
):
    assert session_pool is not None, ValueError("session_pool cannot be None")
    assert sqla_usermodel is not None, ValueError("sqla_usermodel cannot be None")

    print(f"Inserting TestUserModel: ({sqla_usermodel.__repr__()})")
    with session_pool() as session:
        session.add(sqla_usermodel)
        try:
            session.commit()
            print(f"TestUserModel committed successfully")

        except Exception as exc:
            raise Exception(
                f"Unhandled exception committing TestUserModel to database. Details: {exc}\nTestUserModel: {sqla_usermodel.__repr__()}"
            )


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
