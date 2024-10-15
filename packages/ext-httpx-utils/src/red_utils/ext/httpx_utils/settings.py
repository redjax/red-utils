from __future__ import annotations

from dynaconf import Dynaconf

HTTP_SETTINGS = Dynaconf(
    environments=True,
    env="http",
    envvar_prefix="http",
    settings_files=["settings.toml", ".secrets.toml"],
)
