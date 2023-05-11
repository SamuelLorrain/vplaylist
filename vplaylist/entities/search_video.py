from typing import Optional
from enum import Enum, auto
from dataclasses import dataclass, field


class Webm(Enum):
    NO_WEBM = auto()
    ONLY_WEBM = auto()
    ALL = auto()


class Quality(Enum):
    ONLY_SD = auto()
    ONLY_HD = auto()
    ALL = auto()


class Sorting(Enum):
    SQL_RANDOM_FUNCTION = auto()
    ON_RAM_RANDOMIZE = auto()
    LAST_BY_DATE_DOWN = auto()
    LAST_BY_ID = auto()


class SearchType(Enum):
    BASIC = auto()
    NO_SEARCH = auto()
    BEST = auto()


@dataclass
class SearchVideo:
    webm: Webm = field(default=Webm.ALL)
    quality: Quality = field(default=Quality.ALL)
    limit: Optional[int] = field(default=150)
    shift: int = field(default=0)
    sorting: Sorting = field(default=Sorting.LAST_BY_DATE_DOWN)

    should_permutate: bool = field(default=True)
    should_use_synonyms: bool = field(default=True)
    search_term: str = field(default="")
    search_type: SearchType = field(default=SearchType.BASIC)
