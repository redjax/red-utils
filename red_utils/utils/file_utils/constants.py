from __future__ import annotations

from datetime import datetime

default_json_dir: str = "data/json"


def file_ts(fmt: str = "%Y-%m-%d_%H:%M:%S") -> datetime:
    """Return a formatted timestamp, useful for prepending to dir/file names."""
    now: datetime = datetime.now().strftime(fmt)

    return now
