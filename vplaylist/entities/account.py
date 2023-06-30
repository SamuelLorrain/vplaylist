from uuid import UUID
from pydantic import BaseModel


class Account(BaseModel):
    uuid: UUID
    username: str
