from vplaylist.services.video_services import create_thumbnail_for_video, has_thumbnail
from vplaylist.repositories.video_repository import VideoRepository


def generate_thumbnails():
    video_repository = VideoRepository()
    videos = video_repository.get_all_generator()
    for video in videos:
        if not has_thumbnail(video):
            create_thumbnail_for_video(video)
            print(f"generating thumbnails for {video.path}")
