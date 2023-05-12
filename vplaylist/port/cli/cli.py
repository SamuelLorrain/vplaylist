from vplaylist.port.cli.parser import CliParser
from vplaylist.entities.search_video import SearchVideo
from vplaylist.actions.create_playlist import create_playlist
from vplaylist.actions.clean_database import clean_database
from vplaylist.actions.update_database import update_database
from vplaylist.service.play_playlist_service import PlayPlaylistService


class Cli:
    def __init__(self):
        self.parser = CliParser()
        self.args: dict = self.parser.get_args()
        self.route_args()
        # TODO handle "--debug" option

    def route_args(self):
        if self.args["generate"]:
            self.generate_database_controller()
        if self.args["clean_database"]:
            self.clean_database_controller()
        else:
            self.create_playlist_controller()

    def generate_database_controller(self):
        is_successfully_updated = update_database()
        if is_successfully_updated:
            print("database successfully generated!")
        else:
            print("error while generate database!")

    def clean_database_controller(self):
        is_successfully_cleaned = clean_database()
        if is_successfully_cleaned:
            print("database successfully cleaned!")
        else:
            print("error while cleaning database!")

    def create_playlist_controller(self):
        search_video = SearchVideo(
            webm=self.args["webm"],
            quality=self.args["quality"],
            limit=self.args["limit"],
            shift=self.args["shift"],
            sorting=self.args["sorting"],
            search_term=self.args["term"],
            search_type=self.args["search_type"],
        )
        playlist = create_playlist(search_video)

        if self.args["display"]:
            print(playlist)

        if not self.args["no_play"]:
            # FIXME need to inject config somehow
            play_playlist_service = PlayPlaylistService( playlist)
            play_playlist_service.play_playlist()
        else:
            print("no play")
