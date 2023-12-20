from pydantic import BaseModel


class VideoResponse(BaseModel):
    path: str = ""
    uuid: str = ""


class CreatePlaylistResponse(BaseModel):
    playlist: list[VideoResponse] = []
