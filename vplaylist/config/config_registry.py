import os
import sqlite3
import tomllib
from functools import cached_property
from pathlib import Path


class Singleton(type):
    """
    put that here because we don't want to expose a
    singleton interface. I only need a singleton for
    the config class...
    FIXME find a better behavior
    """

    _instances = {}  # type: ignore

    def __call__(cls, *args, **kwargs):  # type: ignore
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class ConfigRegistry(metaclass=Singleton):
    def __init__(self) -> None:
        self.config_file = Path(os.path.dirname(__file__)) / "../../config.toml"
        if not self.config_file.exists():
            raise Exception(f"{self.config_file} not found")

        self.config_file_content = self.config_file.open("r").read()
        self.config = tomllib.loads(self.config_file_content)

    @cached_property
    def db_file(self) -> Path:
        db_file_var = Path(self.config["database"]["db_file"])
        if db_file_var.is_absolute():
            return db_file_var
        return Path(os.path.dirname(__file__)) / "../.." / db_file_var

    @cached_property
    def db_paths(self) -> list[Path]:
        return [Path(path) for path in self.config["database"]["db_paths"]]

    @cached_property
    def ignore_paths(self) -> list[Path]:
        return [Path(path) for path in self.config["database"]["ignore_paths"]]

    @cached_property
    def hard_limit(self) -> int:
        hard_limit = self.config.get("hard_limit")
        if isinstance(hard_limit, int):
            return hard_limit
        return 1500

    @cached_property
    def default_limit(self) -> int:
        default_limit_config = self.config["playlist"]["length"]["default_limit"]
        if not isinstance(default_limit_config, int):
            default_limit_config = 150
        hard_limit_config = self.config["playlist"]["length"]["hard_limit"]
        if not isinstance(hard_limit_config, int):
            hard_limit_config = 1500
        return (
            default_limit_config
            if default_limit_config < hard_limit_config
            else hard_limit_config
        )

    @cached_property
    def synonyms(self) -> list[list[str]]:
        return self.config["search"]["synonyms"]

    @cached_property
    def best(self) -> list[str]:
        connection = sqlite3.connect(self.db_file)
        cursor = connection.execute("select * from data_best_search")
        return [search_term[0] for search_term in cursor.fetchall()]
