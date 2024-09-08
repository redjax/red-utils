from __future__ import annotations

from red_utils.ext import sqlalchemy_utils

import sqlalchemy.orm as so

TEST_BASE: so.DeclarativeBase = sqlalchemy_utils.Base
