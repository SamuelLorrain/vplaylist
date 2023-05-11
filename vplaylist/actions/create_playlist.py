from vplaylist.entities.search_video import SearchVideo
from vplaylist.entities.playlist import Playlist
from vplaylist.service.create_playlist_service import CreatePlaylistService


def create_playlist(search: SearchVideo) -> Playlist:
    create_playlist_service = CreatePlaylistService(search)
    playlist = create_playlist_service.create_playlist()
    return playlist

