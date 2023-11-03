from enum import Enum
import sys
from typing import TextIO


class EnumLogLevels(Enum):
    TRACE: str = "TRACE"
    DEBUG: str = "DEBUG"
    INFO: str = "INFO"
    SUCCESS: str = "SUCCESS"
    WARNING: str = "WARNING"
    ERROR: str = "ERROR"
    CRITICAL: str = "CRITICAL"


class EnumDefaultSinks(Enum):
    STDOUT: TextIO = sys.stdout
    STDERR: TextIO = sys.stderr
    APP_FILE: str = "logs/app.log"
    ERROR_FILE: str = "logs/err.log"
    TRACE_FILE: str = "logs/trace.log"
