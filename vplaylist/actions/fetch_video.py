from uuid import UUID

from vplaylist.app import app
from vplaylist.entities.playlist import Video
from vplaylist.repositories.video_repository import VideoRepository


def fetch_video(uuid: UUID) -> Video:
    video_repository = app(VideoRepository)  # type: ignore
    video = video_repository.fetch_video(uuid)
    return video
