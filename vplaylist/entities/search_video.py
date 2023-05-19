from dataclasses import dataclass, field
from enum import Enum

from vplaylist.config.config_registry import ConfigRegistry


class Webm(str, Enum):
    NO_WEBM = "no_webm"
    ONLY_WEBM = "only_webm"
    ALL = "all"


class Quality(str, Enum):
    ONLY_SD = "sd"
    ONLY_HD = "hd"
    ALL = "all"


class Sorting(str, Enum):
    SQL_RANDOM_FUNCTION = "random_1"
    ON_RAM_RANDOMIZE = "random_2"
    LAST_BY_DATE_DOWN = "last_by_date"
    LAST_BY_ID = "last_by_id"


class SearchType(str, Enum):
    BASIC = "basic"
    NO_SEARCH = "no_search"
    BEST = "best"


@dataclass
class SearchVideo:
    webm: Webm = field(default=Webm.ALL)
    quality: Quality = field(default=Quality.ALL)
    limit: int = field(default=150)
    shift: int = field(default=0)
    sorting: Sorting = field(default=Sorting.LAST_BY_DATE_DOWN)

    should_permutate: bool = field(default=True)
    should_use_synonyms: bool = field(default=True)
    search_term: str = field(default="")
    search_type: SearchType = field(default=SearchType.BASIC)

    def __post_init__(self) -> None:
        self.config_registry = ConfigRegistry()

        # limit rules
        if not self.limit:
            self.limit = self.config_registry.default_limit
        if self.limit > self.config_registry.hard_limit:
            self.limit = self.config_registry.hard_limit
