from typing import Optional
from uuid import UUID

from vplaylist.app import app
from vplaylist.repositories.video_repository import VideoRepository


def modify_video_details(
    uuid: UUID, name: Optional[str], note: Optional[int], date_down: Optional[str]
) -> bool:
    video_repository = app(VideoRepository)  # type: ignore
    video_repository.modify_video(uuid, name, note, date_down)
    return True
