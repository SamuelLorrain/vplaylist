from vplaylist.app import app
from vplaylist.repositories.video_repository import VideoRepository


def clean_collection() -> bool:
    video_repository = app(VideoRepository)  # type: ignore
    return video_repository.clean_non_existent_videos()
