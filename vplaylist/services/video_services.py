import subprocess

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.playlist import Video


def create_thumbnail_for_video(video: Video) -> None:
    config = ConfigRegistry()

    path = config.thumbnail_folder
    if not path.exists():
        path.mkdir()

    fullpath = video.rootpath.path / video.path
    ffmpeg = subprocess.Popen(
        [
            "ffmpeg",
            "-y",
            "-i",
            str(fullpath),
            "-ss",
            "00:00:30.00",
            "-vf",
            "thumbnail=300",
            "-frames:v",
            "1",
            str(config.thumbnail_folder / (video.uuid + ".jpg")),
        ],
    )
    ffmpeg.wait()


def has_thumbnail(video: Video) -> bool:
    config = ConfigRegistry()
    config_path = config.thumbnail_folder / (video.uuid + ".jpg")
    return config_path.exists()
