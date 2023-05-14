from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


@dataclass
class RootPath:
    path: str


@dataclass
class Video:
    path: str
    rootpath: RootPath = field(repr=False)
    height: int
    width: int
    uuid: str = field(default="")
    name: Optional[str] = field(default=None)
    film: Optional[str] = field(default=None)
    date_down: Optional[int] = field(default=None)
    note: Optional[int] = field(default=None)
    lu: bool = field(default=False)

    def getFullPath(self) -> Path:
        return Path(self.rootpath.path + self.path)

    # TODO a a voir avec la persistence
    def isPathValid(self) -> bool:
        return self.getFullPath().exists()


@dataclass
class Playlist:
    playlist: list[Video]
