from pathlib import Path
import os
import tomllib
from functool import cached_property

class ConfigRegistry():
    def __init__(self):
        self.config_file = Path(os.path.dirname(__file__)) / "../../config.toml"
        if not self.config_file.exists():
            raise Exception(f"{self.config_file} not found")

        self.config_file_content = self.config_file.open('r').read()
        self.config = tomllib.loads(self.config_file_content)

    @cached_property
    def db_file(self) -> Path:
        db_file_var =  Path(self.config['database']['db_file'])
        if db_file_var.is_absolute():
            return db_file_var
        return Path(os.path.dirname(__file__)) / "../.." / db_file_var

    @cached_property
    def db_paths(self) -> Path:
        return [Path(path) for path in self.config['database']['db_paths']]

    @cached_property
    def ignore_paths(self) -> Path:
        return [Path(path) for path in self.config['database']['ignore_paths']]

    @cached_property
    def hard_limit(self) -> int:
        return self.config['hard_limit']

    @cached_property
    def default_limit(self) -> int:
        return self.config['default_limit'] if self.config['default_limit'] < self.hard_limit else self.hard_limit

    @cached_property
    def synonyms(self) -> list[list[str]]:
        return self.config['search']['synonyms']

    @cached_property
    def best(self) -> list[str]:
        return self.config['search']['best']
