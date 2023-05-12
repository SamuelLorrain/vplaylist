from vplaylist.entities.playlist import Playlist
from tempfile import NamedTemporaryFile
from vplaylist.service.player import PlayerMPV


class PlayPlaylistService:
    def __init__(self, playlist: Playlist):
        self.playlist = playlist

    def play_playlist(self):
        if len(self.playlist.playlist) < 1:
            print("Empty playlist!")

        print(f"{len(self.playlist.playlist)} found")

        with NamedTemporaryFile(mode="r+", suffix=".m3u") as tmp:
            for i in self.playlist.playlist:
                tmp.write(f"{i.getFullPath()}\n")

            tmp.seek(0)
            self.player = PlayerMPV(tmp)
            self.player.launch_playlist()
