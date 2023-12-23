import sqlite3
from abc import ABC, abstractmethod
from typing import Optional
from uuid import uuid4

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.account import Account
from vplaylist.entities.playlist import RootPath


class AccountRepository(ABC):
    @abstractmethod
    def create(self, username: str, hashed_password: bytes) -> Optional[Account]:
        raise NotImplementedError

    @abstractmethod
    def get_user_by_name(self, username: str) -> Optional[tuple[Account, bytes]]:
        raise NotImplementedError

    @abstractmethod
    def get_rootpath_for_account(self, account: Account) -> list[RootPath]:
        raise NotImplementedError


class SqliteAccountRepository(AccountRepository):
    def __init__(self) -> None:
        self.config_registry = ConfigRegistry()
        self.db_file = self.config_registry.db_file

    def create(self, username: str, hashed_password: bytes) -> Optional[Account]:
        conn = sqlite3.connect(self.db_file)
        new_uuid = uuid4()
        try:
            conn.execute(
                """
                INSERT INTO data_account(uuid, username, password)
                VALUES (?,?,?);
                """,
                (str(new_uuid), username, hashed_password),
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return None
        conn.close()
        return Account(uuid=new_uuid, username=username)

    def get_user_by_name(self, username: str) -> Optional[tuple[Account, bytes]]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.execute(
            """
            SELECT uuid, username, password
            FROM data_account
            WHERE username = ?;
            """,
            (username,),
        )
        result = cursor.fetchone()
        conn.close()
        if result is not None:
            return (Account(uuid=result[0], username=result[1]), result[2])
        return None

    def get_rootpath_for_account(self, account: Account) -> list[RootPath]:
        conn = sqlite3.connect(self.db_file)
        cursor = conn.execute(
            """
            SELECT id,path
            FROM data_rootpath
            JOIN account_rootpath ON data_rootpath.id = account_rootpath.rootpath_id
            WHERE account_uuid = ?;
            """,
            (str(account.uuid),),
        )
        result = [RootPath(id=row[0], path=row[1]) for row in cursor.fetchall()]
        conn.close()
        return result
