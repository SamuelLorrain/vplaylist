from vplaylist.app import app
from vplaylist.repositories.video_repository import VideoRepository


def update_collection() -> bool:
    video_repository = app(VideoRepository)  # type: ignore
    return video_repository.insert_new_videos()
