from red_utils.ext import sqlalchemy_utils

import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from pytest import fixture

@fixture
def sqla_base() -> DeclarativeAttributeIntercept:
    return sqlalchemy_utils.Base
