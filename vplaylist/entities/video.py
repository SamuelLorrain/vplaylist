from datetime import date
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Studio(BaseModel):
    name: str


class Film(BaseModel):
    name: str


class Tag(BaseModel):
    name: str
    note: Optional[int]


class Participant(BaseModel):
    name: str
    tags: list[Tag]
    note: Optional[int]


class VideoDetails(BaseModel):
    uuid: UUID
    name: Optional[str]
    participants: Optional[list[Participant]]
    film: Optional[Film]
    studio: Optional[Studio]
    tags: list[Tag]
    date_down: Optional[date]
    lu: Optional[bool]
    height: Optional[int]
    width: Optional[int]
    note: Optional[int]
