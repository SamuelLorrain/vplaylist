import json
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.account import Account


def hash_password(password: str) -> bytes:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(password_bytes, salt)
    return hash


def verify_password(password: bytes, hash_to_verify: bytes) -> bool:
    return bcrypt.checkpw(password, hash_to_verify)


def get_expiration_date() -> str:
    return str(round((datetime.now() + timedelta(days=7)).timestamp()))


def get_new_token(account: Account) -> Optional[str]:
    config_registry = ConfigRegistry()
    if not account:
        return None
    return jwt.encode(
        {
            "username": account.username,
            "uuid": str(account.uuid),
            "exp": get_expiration_date(),
        },
        config_registry.jwt_secret,
        algorithm="HS256",
    )


def extends_token(token: str) -> Optional[str]:
    config_registry = ConfigRegistry()
    try:
        new_token = json.loads(
            jwt.decode(token, config_registry.jwt_secret, algorithms=["HS256"])
        )
        new_token["exp"] = get_expiration_date()
        return jwt.encode(new_token, config_registry.jwt_secret, algorithm="HS256")
    except jwt.exceptions.DecodeError as e:
        print(e)
        return None


def is_token_valid(token: bytes) -> bool:
    config_registry = ConfigRegistry()
    try:
        jwt.decode(token, config_registry.jwt_secret, algorithms=["HS256"])
        return True
    except jwt.exceptions.DecodeError:
        return False
    except jwt.exceptions.ExpiredSignatureError:
        return False


def get_username_from_token(token: bytes) -> Optional[str]:
    config_registry = ConfigRegistry()
    decoded = jwt.decode(token, config_registry.jwt_secret, algorithms=["HS256"])
    username = decoded.get("username")
    if username is not None and not isinstance(username, str):
        raise Exception("Invalid username")
    return username
