from vplaylist.entities.search_video import (
    Webm,
    Quality,
    Sorting
)
import argparse

DEFAULT_LIMIT = 150
HARD_LIMIT = 300


class CliParser: def __init__(self):
        self.parser = argparse.ArgumentParser(description="vplaylist 2nd version")
        self.args = {}
        self._init_parser_config()
        self.args = vars(self.parser.parse_args())

    def get_args(self) -> dict:
        return self.args

    def _init_search_video_parser_config():
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
            default=DEFAULT_LIMIT,
            dest="limit",
            help=f"limit number of vids (by default {DEFAULT_LIMIT}",
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
            help="give lasts vids"
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
            "--no-play", action="store_const", const=True, default=False, help="don't play"
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

    def _init_generate_db_parser_config() -> None:
        self.parser.add_argument(
            "-g",
            "--generate",
            action="store_const",
            const=True,
            dest="generate",
            default=False,
            help="generate DB",
        )

    def _init_clean_db_parser_config() -> None:
        self.parser.add_argument(
            "--clean-database",
            action="store_const",
            const=True,
            dest="clean_database",
            default=False,
            help="clean database",
        )

    def _init_config_db_parser_config() -> None:
        self.parser.add_argument(
            "--debug", action="store_const", const=True, default=False, help="show debug informations"
        )

    def _init_parser_config(self) -> None:
        _init_search_video_parser_config()
        _init_generate_db_parser_config()
        _init_clean_db_parser_config()
