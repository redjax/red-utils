import sys

sys.path.append(".")

from .schemas import SQLiteDB
from .operations import init_sqlite_db, get_demo_db, get_sqlite_db
