from __future__ import annotations

import uuid

from pydantic import BaseModel, Field, ValidationError, field_validator

class TestUserBase(BaseModel):
    username: str = Field(default=None)
    email: str | None = Field(default=None)
    description: str | None = Field(default=None)


class TestUser(TestUserBase):
    pass


class TestUserOut(TestUserBase):
    id: uuid.UUID = Field(default=None, alias="user_id")
