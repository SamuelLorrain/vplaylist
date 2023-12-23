from typing import Annotated, Optional
from uuid import UUID

from fastapi import Header, HTTPException

from vplaylist.entities.account import Account
from vplaylist.repositories.account_repository import AccountRepository
from vplaylist.repositories.video_repository import VideoRepository
from vplaylist.services.authentication_service import (
    get_username_from_token,
    is_token_valid,
)


def get_token_from_authorization_header(authorization: Optional[str]) -> str:
    if authorization is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    try:
        token = authorization[7:]
    except IndexError as err:
        raise HTTPException(status_code=403, detail="Not authenticated") from err
    if not is_token_valid(token.encode("utf8")):
        raise HTTPException(status_code=403, detail="Not authenticated")
    return token


def get_account(authorization: Annotated[Optional[str], Header()] = None) -> Account:
    account_repository = AccountRepository()
    token = get_token_from_authorization_header(authorization)
    username = get_username_from_token(token.encode("utf8"))
    if username is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    account_and_password = account_repository.get_user_by_name(username)
    if account_and_password is None:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return account_and_password[0]


def authorize_video_uuid(
    uuid: UUID, authorization: Annotated[Optional[str], Header()] = None
) -> UUID:
    video_repository = VideoRepository()
    account_repository = AccountRepository()
    account = get_account(authorization)
    if video_repository.video_is_in_rootpath(
        uuid, account_repository.get_rootpath_for_account(account)
    ):
        return uuid
    raise HTTPException(status_code=403, detail="Forbidden")
