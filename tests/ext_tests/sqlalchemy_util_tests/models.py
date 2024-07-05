from __future__ import annotations

import uuid

from .base import TEST_BASE

from red_utils.ext import sqlalchemy_utils
from red_utils.std import uuid_utils
import sqlalchemy as sa
import sqlalchemy.orm as so


class TestUserModel(
    TEST_BASE,
    sqlalchemy_utils.mixins.TableNameMixin,
    sqlalchemy_utils.mixins.TimestampMixin,
):
    # type_annotation_map = {uuid.UUID: sqlalchemy_utils.CompatibleUUID}
    type_annotation_map = sqlalchemy_utils.custom_types.TYPEMAP_COMPATIBLE_UUID

    user_id: so.Mapped[uuid.UUID] = so.mapped_column(
        primary_key=True, nullable=False, insert_default=uuid.uuid4
    )
    username: so.Mapped[str] = so.mapped_column(sa.VARCHAR(32), nullable=False)
    email: so.Mapped[str | None] = so.mapped_column(sa.VARCHAR(64), nullable=True)
    description: so.Mapped[sqlalchemy_utils.custom_types.STR_255]

    def __repr__(self):
        return f"user_id={self.user_id!r}, username={self.username!r}, email={self.email!r}, description={self.description!r}"


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
