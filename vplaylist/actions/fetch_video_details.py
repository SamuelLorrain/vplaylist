from typing import Optional
from uuid import UUID

from vplaylist.entities.video import VideoDetails
from vplaylist.repositories.video_repository import VideoRepository


def fetch_video_details(uuid: UUID) -> Optional[VideoDetails]:
    video_repository = VideoRepository()
    video_details = video_repository.fetch_video_details(uuid)
    return video_details
