from __future__ import annotations

import uuid

from pydantic import BaseModel, Field, ValidationError, field_validator, ConfigDict


class TestUserBase(BaseModel):
    username: str = Field(default=None)
    email: str | None = Field(default=None)
    description: str | None = Field(default=None)


class TestUser(TestUserBase):
    pass


class TestUserOut(TestUserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID = Field(default=None, alias="user_id")


class TestUserUpdate(TestUserBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID = Field(default=None, exclude=True)
    username: str | None
    email: str | None
    description: str | None
