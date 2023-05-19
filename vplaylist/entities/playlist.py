import io
import os
from dataclasses import dataclass, field
from functools import cached_property
from pathlib import Path
from typing import Optional

from vplaylist.exceptions.validation_error import ValidationError


@dataclass
class RootPath:
    path: Path


@dataclass
class Video:
    path: Path
    height: int
    width: int
    rootpath: RootPath = field(repr=False)  # rootpath is aggregated to a video
    uuid: str = field(default="")
    name: Optional[str] = field(default=None)
    film: Optional[str] = field(default=None)
    date_down: Optional[int] = field(default=None)
    note: Optional[int] = field(default=None)
    lu: bool = field(default=False)

    def __post_init__(self) -> None:
        if not self.fullpath.exists():
            raise ValidationError(f"path must exist: {self.fullpath}")
        if self.fullpath.is_dir():
            raise ValidationError(f"path must not be a directory: {self.fullpath}")

    @cached_property
    def fullpath(self) -> Path:
        return Path(self.rootpath.path / self.path)

    @cached_property
    def media_type(self) -> str:
        return f"video/{self.fullpath.suffix[1:]}"

    @cached_property
    def size(self) -> int:
        return os.path.getsize(str(self.fullpath))

    @cached_property
    def stream(self) -> io.FileIO:
        return io.FileIO(str(self.fullpath), "br")


Playlist = list[Video]
