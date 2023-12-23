from typing import Optional

from vplaylist.app import app
from vplaylist.entities.account import Account
from vplaylist.repositories.account_repository import AccountRepository
from vplaylist.services.authentication_service import verify_password


def verify_account(username: str, password: str) -> Optional[Account]:
    account_repository = app(AccountRepository)  #  type: ignore
    account_and_hash = account_repository.get_user_by_name(username)
    if account_and_hash is None:
        return None
    if verify_password(password.encode("utf-8"), account_and_hash[1]):
        return account_and_hash[0]
    return None
