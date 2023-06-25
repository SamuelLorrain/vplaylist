from pathlib import Path
from uuid import UUID

from vplaylist.config.config_registry import ConfigRegistry


def fetch_video_thumbnail_from_uuid(uuid: UUID) -> Path:
    config = ConfigRegistry()
    folder = config.thumbnail_folder
    return Path(folder / (str(uuid) + '.jpg'))
