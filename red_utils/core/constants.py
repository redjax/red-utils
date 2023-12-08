from pathlib import Path

DATA_DIR: Path = Path(".data")
CACHE_DIR: Path = Path(".cache")
SERIALIZE_DIR: Path = Path(".serialize")
JSON_DIR: Path = Path(f"{DATA_DIR}/json")

ENSURE_EXIST_DIRS: list[Path] = [DATA_DIR, CACHE_DIR, SERIALIZE_DIR]