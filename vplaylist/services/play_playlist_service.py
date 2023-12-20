from tempfile import NamedTemporaryFile

from vplaylist.entities.playlist import Playlist
from vplaylist.services.player import Player
from vplaylist.app import App


class PlayPlaylistService:
    def __init__(self, playlist: Playlist) -> None:
        self.playlist: Playlist = playlist
        self.player: Player = App().app(Player)

    def play_playlist(self) -> None:
        if len(self.playlist) < 1:
            print("Empty playlist!")

        print(f"{len(self.playlist)} found")

        with NamedTemporaryFile(mode="r+", suffix=".m3u") as tmp:
            for video in self.playlist:
                tmp.write(f"{video.fullpath}\n")

            tmp.seek(0)
            self.player.set_playlist(tmp)
            self.player.launch_playlist()
