import io
import os
from dataclasses import dataclass
from pathlib import Path

from vplaylist.exceptions.validation_exception import ValidationException


@dataclass
class PlayableVideo:
    fullpath: Path

    def __post_init__(self) -> None:
        if not self.fullpath.exists():
            raise ValidationException(f"path must exist: {self.fullpath}")
        if self.fullpath.is_dir():
            raise ValidationException(f"path must not be a directory: {self.fullpath}")

    def get_media_type(self) -> str:
        return f"video/{self.fullpath.suffix[1:]}"

    def get_size(self) -> int:
        return os.path.getsize(str(self.fullpath))

    def get_stream(self) -> io.FileIO:
        return io.FileIO(str(self.fullpath), "br")
