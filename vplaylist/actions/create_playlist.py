from vplaylist.entities.playlist import Playlist
from vplaylist.entities.search_video import SearchVideo
from vplaylist.repositories.playlist_repository import PlaylistRepository


def create_playlist(search: SearchVideo) -> Playlist:
    playlist_repository = PlaylistRepository()
    playlist = playlist_repository.create_playlist(search)
    return playlist
