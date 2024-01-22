from __future__ import annotations

from .base import TEST_BASE
from .methods import (
    create_base_metadata,
    get_list_user_schemas,
    get_user_schema,
    insert_testusermodel,
)
from .models import TestUserModel
from .schemas import TestUser, TestUserOut

from pytest import mark, xfail
from red_utils.ext import sqlalchemy_utils
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

EX_TESTUSERMODEL_FULL: TestUserModel = TestUserModel(
    username="TestUser1",
    email="test@example.com",
    description="This is a TestUserModel instance created for use in Pytest.",
)
EX_TESTUSERMODEL_LIST: list[TestUserModel] = [
    TestUserModel(
        username="TestListUser1", description="A TestUser in a list for Pytest"
    ),
    TestUserModel(
        username="TestListUser2",
        email="test2@example.com",
        description="A second TestUser in a list for Pytest",
    ),
    TestUserModel(
        username="TestListUser3",
        email="test3@example.com",
        description="A third TestUser in a list for Pytest",
    ),
]


def initialize_test_db(
    engine: sa.Engine,
    base: so.DeclarativeBase = TEST_BASE,
    insert_models: list[TestUserModel] = EX_TESTUSERMODEL_LIST,
):
    base.metadata.create_all(bind=engine)

    SessionLocal: so.sessionmaker[so.Session] = so.sessionmaker(bind=engine)

    for model in insert_models:
        insert_testusermodel(session_pool=SessionLocal, sqla_usermodel=model)


@mark.sqla_utils
def test_user_schema():
    user: TestUser = get_user_schema()

    print(f"TestUser schema: {user}")


@mark.sqla_utils
def test_convert_user_schema_to_model():
    user: TestUser = get_user_schema()

    try:
        user_model: TestUserModel = TestUserModel(
            username=user.username, email=user.email, description=user.description
        )
        print(
            f"TestUser schema converted to TestUserModel successfully.\n\tSchema: {user}\n\tModel: {user_model.__repr__()}"
        )

    except Exception as exc:
        raise Exception(
            f"Unhandled exception converting TestUser schema to TestUserModel. Detail: {exc}"
        )


@mark.sqla_utils
def test_sqla_create_base_metadata(
    sqla_sqlite_engine: sa.Engine,
    sqla_base: so.DeclarativeBase = TEST_BASE,
):
    create_base_metadata(sqla_engine=sqla_sqlite_engine, sqla_base=sqla_base)


@mark.sqla_utils
def test_sqla_list_tables(
    sqla_sqlite_engine, sqla_base: so.DeclarativeBase = TEST_BASE
):
    create_base_metadata(sqla_engine=sqla_sqlite_engine, sqla_base=sqla_base)
    tables = sqla_base.metadata.tables.keys()

    print(f"Database tables: {tables}")


@mark.sqla_utils
def test_sqla_sqlite_session_pool(sqla_session: so.sessionmaker[so.Session]):
    with sqla_session() as session:
        session.execute(sa.text("SELECT 1"))


@mark.sqla_utils
def test_sqla_create_usermodel(sqla_usermodel: TestUserModel = EX_TESTUSERMODEL_FULL):
    sqla_usermodel: TestUserModel = TestUserModel(
        username="TestUser1",
        email="test@example.com",
        description="This is a TestUserModel instance created for use in Pytest.",
    )
    print(f"TestUserModel: {sqla_usermodel.__repr__()}")

    usermodel_schema: TestUser = TestUser.model_validate(sqla_usermodel.__dict__)
    print(f"TestUser schema: {usermodel_schema}")


@mark.sqla_utils
def test_sqla_insert_user(
    sqla_sqlite_engine: sa.Engine,
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodel=EX_TESTUSERMODEL_FULL,
):
    try:
        initialize_test_db(
            engine=sqla_sqlite_engine, base=sqla_base, insert_models=[sqla_usermodel]
        )
        
    except Exception as exc:
        raise Exception(f"Unhandled exception inserting TestUserModel into database. Details: {exc}")


@mark.sqla_utils
def test_sqla_select_all_users(
    sqla_session: so.sessionmaker[so.Session],
    sqla_sqlite_engine: so.sessionmaker[so.Session],
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: list[TestUserModel] = EX_TESTUSERMODEL_LIST,
):
    initialize_test_db(engine=sqla_sqlite_engine, base=sqla_base, insert_models=sqla_usermodels)

    with sqla_session() as session:
        # users = session.execute(sa.text("SELECT * FROM testusermodels;")).all()
        users = session.query(TestUserModel).all()
        print(f"All TestUserModels in database ({type(users)}): {users}")
        
        for user in users:
            print(f"SELECT TestUserModel ({type(user)}): {user}")
            
            try:
                user_schema: TestUserOut = TestUserOut.model_validate(user.__dict__)
                print(f"SELECT TestUserOut: {user_schema}")
            except Exception as exc:
                raise Exception(f"Unhandled exception converting TestUserModel to TestUserOut schema. Details: {exc}")
