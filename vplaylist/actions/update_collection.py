from vplaylist.repositories.video_repository import VideoRepository


def update_collection() -> bool:
    video_repository = VideoRepository()
    return video_repository.insert_new_videos()
