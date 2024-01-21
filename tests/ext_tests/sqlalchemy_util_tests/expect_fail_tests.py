import sqlalchemy as sa
import sqlalchemy.orm as so

from sqlalchemy.orm.decl_api import DeclarativeAttributeIntercept

from pytest import mark, xfail
from red_utils.ext import sqlalchemy_utils

@mark.xfail
@mark.sqla_utils
def test_fail_sqla_base(sqla_base: so.DeclarativeBase):
    assert sqla_base is not None, ValueError("Missing sqla_base")
    assert isinstance(sqla_base, so.DeclarativeBase), TypeError(f"Expected failure, sqla_base is not of type DeclarativeAttributeIntercept. Type: ({type(sqla_base)})")