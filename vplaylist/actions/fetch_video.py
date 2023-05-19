from uuid import UUID

from vplaylist.entities.playlist import Video
from vplaylist.repositories.video_repository import VideoRepository


def fetch_video(uuid: UUID) -> Video:
    video_repository = VideoRepository()
    video = video_repository.fetch_video(uuid)
    return video
