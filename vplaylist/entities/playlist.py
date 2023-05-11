from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class RootPath:
    path: str


@dataclass
class Video:
    path: str
    rootpath: RootPath = field(repr=False)
    height: int
    width: int
    name: str = field(default=None)
    film: str = field(default=None)
    date_down: int = field(default=None)
    note: int = field(default=None)
    lu: bool = field(default=False)

    def getFullPath(self) -> Path:
        return Path(self.rootpath.path + self.path)

    # TODO a a voir avec la persistence
    def isPathValid(self) -> bool:
        return self.getFullPath().exists()


@dataclass
class Playlist:
    playlist: List[Video]
