import sqlite3

from vplaylist.config.config_registry import ConfigRegistry


# TODO should refacto this
class DatabaseService:
    def __init__(self) -> None:
        self.config_registry = ConfigRegistry()
        self.db_file = self.config_registry.db_file
        self.db_paths = self.config_registry.db_paths
        self.ignore_paths = self.config_registry.ignore_paths

    def add_rootpath_from_list(self) -> None:
        db_connection = sqlite3.connect(self.db_file)
        for path in self.db_paths:
            db_connection.execute(
                "INSERT OR IGNORE INTO data_rootpath(path) VALUES (?)",
                (str(path),)
            )
        db_connection.commit()
        db_connection.close()
