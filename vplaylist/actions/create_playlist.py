from vplaylist.app import app
from vplaylist.entities.account import Account
from vplaylist.entities.playlist import Playlist
from vplaylist.entities.search_video import SearchVideo
from vplaylist.repositories.account_repository import AccountRepository
from vplaylist.repositories.playlist_repository import PlaylistRepository


def create_playlist(account: Account, search: SearchVideo) -> Playlist:
    playlist_repository = app(PlaylistRepository)  # type: ignore
    account_repository = app(AccountRepository)  # type: ignore
    rootpaths = account_repository.get_rootpath_for_account(account)
    playlist = playlist_repository.create_playlist(search, rootpaths)
    return playlist
