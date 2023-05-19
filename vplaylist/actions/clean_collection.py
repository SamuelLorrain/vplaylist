from vplaylist.repositories.video_repository import VideoRepository


def clean_collection() -> bool:
    video_repository = VideoRepository()
    return video_repository.clean_non_existent_videos()
