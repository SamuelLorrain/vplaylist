from uuid import UUID
from vplaylist.entities.video import VideoDetails
from vplaylist.repositories.video_repository import VideoRepository


def modify_video_details(uuid: UUID, details: VideoDetails):
    video_repository = VideoRepository()
    video_repository.modify_video(uuid, details)
