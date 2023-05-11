from vplaylist.actions.create_playlist import create_playlist
from vplaylist.entities import SearchVideo

def test__create_playlist():
    search_video = SearchVideo()
    playlist = create_playlist(search_video)

