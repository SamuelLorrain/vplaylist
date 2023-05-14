from uuid import UUID

from vplaylist.entities.video_file import PlayableVideo
from vplaylist.service.database import DatabaseService


def fetch_playable_video(uuid: UUID) -> PlayableVideo:
    database_service = DatabaseService()
    video_path = database_service.fetch_video_from_uuid(uuid)
    fullpath = video_path.rootpath / video_path.path
    video = PlayableVideo(fullpath=fullpath)
    return video
