from vplaylist.entities.playlist import Playlist
from tempfile import NamedTemporaryFile
import subprocess

def play_playlist(playlist: Playlist):
    if len(playlist.playlist) < 1:
        print("Empty playlist!")

    print(f"{len(playlist.playlist)} found")

    with NamedTemporaryFile(mode="r+", suffix=".m3u") as tmp:
        for i in playlist.playlist:
            tmp.write(f"{i.getFullPath()}\n")

        tmp.seek(0)
        subprocess.run(["vlc", tmp.name])
