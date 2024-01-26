from __future__ import annotations

from red_utils.ext import sqlalchemy_utils
from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

TEST_BASE: DeclarativeAttributeIntercept = sqlalchemy_utils.Base
