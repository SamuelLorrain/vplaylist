from dataclasses import dataclass
from pathlib import Path
import io
import os

@dataclass
class PlayableVideo:
    fullpath: Path

    def __post_init__(self):
        if not self.fullpath.exists():
            raise ValidationError(f"path must exist: {v}")
        if self.fullpath.is_dir():
            raise ValidationError(f"path must not be a directory: {v}")

    def get_media_type(self):
        return f"video/{self.fullpath.suffix[1:]}"

    def get_size(self):
        return os.path.getsize(str(self.fullpath))

    def get_stream(self):
        return io.FileIO(str(self.fullpath), 'br')






