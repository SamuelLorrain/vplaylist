from vplaylist.repositories.video_repository import VideoRepository


def modify_video_details(uuid, name):
    video_repository = VideoRepository()
    video = video_repository.fetch_video(uuid)
    video.name = name
    video_repository.modify_video(video)
