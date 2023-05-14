import argparse
from typing import Any

from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.entities.search_video import Quality, SearchType, Sorting, Webm


class CliParser:
    def __init__(self) -> None:
        self.config = ConfigRegistry()
        self.parser = argparse.ArgumentParser(description="vplaylist 2nd version")
        self._init_parser_commands()
        self.args: dict[str, Any] = vars(self.parser.parse_args())

    def get_args(self) -> dict[str, Any]:
        return self.args

    def _init_search_video_parser_commands(self) -> None:
        self.parser.add_argument(
            "--webm",
            "--only-webm",
            action="store_const",
            dest="webm",
            const=Webm.ONLY_WEBM,
            default=Webm.ALL,
            help="only webms",
        )
        self.parser.add_argument(
            "--no-webm",
            action="store_const",
            dest="webm",
            const=Webm.NO_WEBM,
            default=Webm.ALL,
            help="no webms",
        )
        self.parser.add_argument(
            "-hd",
            "--hd",
            "--only-hd",
            action="store_const",
            dest="quality",
            const=Quality.ONLY_HD,
            help="only hd vids",
            default=Quality.ALL,
        )
        self.parser.add_argument(
            "-sd",
            "--sd",
            "--only-sd",
            action="store_const",
            dest="quality",
            const=Quality.ONLY_SD,
            help="only sd vids",
            default=Quality.ALL,
        )
        self.parser.add_argument(
            "--limit",
            nargs="?",
            type=int,
            default=self.config.default_limit,
            dest="limit",
            help=f"limit number of vids (by default {self.config.default_limit}",
        )
        self.parser.add_argument(
            "-s",
            "--shift",
            nargs="?",
            type=int,
            default=0,
            dest="shift",
            help="shift things",
        )
        self.parser.add_argument(
            "-l",
            "--last",
            action="store_const",
            dest="sorting",
            const=Sorting.LAST_BY_DATE_DOWN,
            default=Sorting.SQL_RANDOM_FUNCTION,
            help="give lasts vids",
        )
        self.parser.add_argument(
            "--last-by-id",
            action="store_const",
            dest="sorting",
            const=Sorting.LAST_BY_ID,
            default=Sorting.SQL_RANDOM_FUNCTION,
            help="give lasts vids by id",
        )
        self.parser.add_argument(
            "--shuffle",
            action="store_const",
            dest="sorting",
            const=Sorting.ON_RAM_RANDOMIZE,
            default=Sorting.SQL_RANDOM_FUNCTION,
            help="force to shuffle vids",
        )
        self.parser.add_argument("term", nargs="?", default=".*", help="term to search")
        self.parser.add_argument(
            "--no-play",
            action="store_const",
            const=True,
            default=False,
            help="don't play",
        )
        self.parser.add_argument(
            "--display-playlist",
            action="store_const",
            const=True,
            dest="display",
            default=False,
            help="Display the full playlist",
        )
        self.parser.add_argument(
            "--best",
            action="store_const",
            dest="search_type",
            const=SearchType.BEST,
            default=SearchType.BASIC,
            help="best based on config",
        )

    def _init_generate_db_parser_commands(self) -> None:
        self.parser.add_argument(
            "-g",
            "--generate",
            action="store_const",
            const=True,
            dest="generate",
            default=False,
            help="generate DB",
        )

    def _init_clean_db_parser_commands(self) -> None:
        self.parser.add_argument(
            "--clean-database",
            action="store_const",
            const=True,
            dest="clean_database",
            default=False,
            help="clean database",
        )

    def _init_administration_db_parser_commands(self) -> None:
        self.parser.add_argument(
            "--debug",
            action="store_const",
            const=True,
            default=False,
            help="show debug informations",
        )

    def _init_parser_commands(self) -> None:
        self._init_search_video_parser_commands()
        self._init_generate_db_parser_commands()
        self._init_clean_db_parser_commands()
