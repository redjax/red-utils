from __future__ import annotations

from .base import TEST_BASE
from .methods import (
    create_base_metadata,
    get_list_user_schemas,
    get_user_schema,
    insert_testusermodel,
)
from .models import TestUserModel
from .schemas import TestUser, TestUserOut, TestUserUpdate

from loguru import logger as log
from pytest import mark, xfail
from red_utils.ext import sqlalchemy_utils
from red_utils.ext.loguru_utils import LoguruSinkStdOut, init_logger
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

init_logger([LoguruSinkStdOut(level="DEBUG").as_dict()])

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
    log.info(
        f"Initializing database & seeding with [{len(insert_models)}] TestUserModel(s)"
    )
    try:
        base.metadata.create_all(bind=engine)
        log.success("Table metadata created")
    except Exception as exc:
        msg = Exception(f"Unhandled exception initializing database. Details: {exc}")
        log.error(msg)

        raise msg

    SessionLocal: so.sessionmaker[so.Session] = so.sessionmaker(bind=engine)

    log.info(f"Inserting [{len(insert_models)}] TestUserModel(s) into the database")
    for model in insert_models:
        try:
            insert_testusermodel(session_pool=SessionLocal, sqla_usermodel=model)
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception inserting TestUserModel into database. TestUserModel object: {model}. Details: {exc}"
            )
            log.error(msg)


@mark.sqla_utils
def test_user_schema():
    user: TestUser = get_user_schema()
    log.success(f"TestUser schema: {user}")


@mark.sqla_utils
def test_convert_user_schema_to_model():
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

    log.info(f"Database tables: {tables}")


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
    log.info(f"TestUserModel: {sqla_usermodel.__repr__()}")

    usermodel_schema: TestUser = TestUser.model_validate(sqla_usermodel.__dict__)
    log.info(f"TestUser schema: {usermodel_schema}")


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
        msg = Exception(
            f"Unhandled exception inserting TestUserModel into database. Details: {exc}"
        )
        log.error(msg)

        raise msg


@mark.sqla_utils
def test_sqla_select_all_users(
    sqla_session: so.sessionmaker[so.Session],
    sqla_sqlite_engine: so.sessionmaker[so.Session],
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: list[TestUserModel] = EX_TESTUSERMODEL_FULL,
):
    initialize_test_db(
        engine=sqla_sqlite_engine, base=sqla_base, insert_models=[sqla_usermodels]
    )

    with sqla_session() as session:
        # users = session.execute(sa.text("SELECT * FROM testusermodels;")).all()
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


@mark.sqla_utils
def test_update_user(
    sqla_session: so.sessionmaker[so.Session],
    sqla_sqlite_engine: so.sessionmaker[so.Session],
    sqla_base: so.DeclarativeBase = TEST_BASE,
    sqla_usermodels: TestUserModel = EX_TESTUSERMODEL_FULL,
):
    initialize_test_db(
        engine=sqla_sqlite_engine, base=sqla_base, insert_models=[sqla_usermodels]
    )

    with sqla_session() as session:
        try:
            usermodel: TestUserModel = session.query(TestUserModel).one()
            log.info(f"SELECT TestUserModel: {usermodel.__dict__}")
        except Exception as exc:
            raise Exception(
                f"Unhandled exception selecting TestUserModel from database. Details: {exc}"
            )

        userschema: TestUserUpdate = TestUserUpdate.model_validate(usermodel)

        log.info(f"User schema before update: {userschema}")
        userschema.description = "This is an updated description!"
        log.info(f"User schema after update: {userschema}")

        for field, value in userschema:
            setattr(usermodel, field, value)

        log.info(f"Updated TestUserModel: {usermodel.__dict__}")

        try:
            session.commit()
        except Exception as exc:
            raise Exception(
                f"Unhandled exception updating User with ID [{userschema.id}]. Details: {exc}"
            )

        updated_usermodel = (
            session.query(TestUserModel)
            .where(TestUserModel.user_id == usermodel.user_id)
            .one()
        )
        updated_userschema: TestUserOut = TestUserOut.model_validate(updated_usermodel)
        log.info(f"SELECT updated TestUserModel: {updated_userschema}")


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
            usermodel: TestUserModel = session.query(TestUserModel).one()
            log.info(f"SELECT TestUserModel: {usermodel.__dict__}")
        except Exception as exc:
            raise Exception(
                f"Unhandled exception selecting TestUserModel from database. Details: {exc}"
            )

        userschema: TestUserOut = TestUserOut.model_validate(usermodel)
        log.info(f"Deleting User: {userschema}")

        try:
            session.delete(usermodel)
            log.success(f"Deleted TestUserModel with ID [{usermodel.user_id}]")
        except Exception as exc:
            msg = Exception(
                f"Unhandled exception deleting TestUserModel with ID [{usermodel.user_id}]. Test User: {userschema}. Details: {exc}"
            )
            log.error(msg)

            raise msg

        session.commit()


## TODO: Expect fail:
#   - [x] create table metadata
#   - [x] insert
#   - [x] update
#   - [ ] delete
