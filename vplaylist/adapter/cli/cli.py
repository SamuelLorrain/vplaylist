from uuid import UUID

from vplaylist.actions.clean_collection import clean_collection
from vplaylist.actions.create_playlist import create_playlist
from vplaylist.actions.generate_thumbnails import generate_thumbnails
from vplaylist.actions.update_collection import update_collection
from vplaylist.adapter.cli.parser import CliParser
from vplaylist.entities.account import Account
from vplaylist.entities.search_video import SearchVideo
from vplaylist.services.play_playlist_service import PlayPlaylistService


class Cli:
    def __init__(self) -> None:
        self.parser = CliParser()
        self.args = self.parser.get_args()
        self.route_args()
        # TODO handle "--debug" option

    def route_args(self) -> None:
        if self.args["generate"]:
            self.update_collection_action()
        elif self.args["clean_database"]:
            self.clean_collection_action()
        elif self.args["generate_thumbnails"]:
            self.generate_thumbnails_action()
        else:
            self.create_playlist_action()

    def update_collection_action(self) -> None:
        is_successfully_updated = update_collection()
        if is_successfully_updated:
            print("database successfully generated!")
        else:
            print("error while generate database!")

    def clean_collection_action(self) -> None:
        is_successfully_cleaned = clean_collection()
        if is_successfully_cleaned:
            print("database successfully cleaned!")
        else:
            print("error while cleaning database!")

    def generate_thumbnails_action(self) -> None:
        print("generating thumbnails NOT WORKING")
        generate_thumbnails()

    def create_playlist_action(self) -> None:
        search_video = SearchVideo(
            webm=self.args["webm"],
            quality=self.args["quality"],
            limit=self.args["limit"],
            shift=self.args["shift"],
            sorting=self.args["sorting"],
            search_term=self.args["term"],
            search_type=self.args["search_type"],
        )
        account = Account(
            username="test", uuid=UUID("76869f95-4e36-4c22-8549-680be32fc20c")
        )
        playlist = create_playlist(account, search_video)

        if self.args["display"]:
            print(playlist)

        if not self.args["no_play"]:
            play_playlist_service = PlayPlaylistService(playlist)
            play_playlist_service.play_playlist()
        else:
            print("no play")
