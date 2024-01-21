import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from pytest import mark, xfail
from red_utils.ext import sqlalchemy_utils

@mark.sqla_utils
def test_sqla_base(sqla_base: so.DeclarativeBase):
    assert sqla_base is not None, ValueError("Missing a SQLAlchemy DeclarativeBase object")
    assert isinstance(sqla_base, so.DeclarativeBase) or isinstance(sqla_base, DeclarativeAttributeIntercept), TypeError(f"sqla_base must be of type sqlalchemy.orm.DeclarativeBase, not ({type(sqla_base)})")
