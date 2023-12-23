from typing import Optional

from vplaylist.entities.account import Account
from vplaylist.repositories.account_repository import AccountRepository
from vplaylist.services.authentication_service import hash_password


def create_new_account(username: str, password: str) -> Optional[Account]:
    account_repository = AccountRepository()
    hashed_password = hash_password(password)
    account = account_repository.create(username, hashed_password)
    return account
