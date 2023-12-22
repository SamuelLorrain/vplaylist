from uuid import UUID
from typing import Optional

from vplaylist.entities.video import VideoDetails
from vplaylist.repositories.video_repository import VideoRepository


def modify_video_details(uuid: UUID, name: Optional[str], note: Optional[int], date_down: Optional[str]) -> bool:
    video_repository = VideoRepository()
    video_repository.modify_video(uuid, name, note, date_down)
    return True
