from vplaylist.adapter.cli.cli import Cli
from vplaylist.app import App

from vplaylist.services.player import Player, PlayerVLC
from vplaylist.repositories.account_repository import AccountRepository, SqliteAccountRepository
from vplaylist.repositories.analytics_repository import AnalyticsRepository, SqliteAnalyticsRepository 
from vplaylist.repositories.participant_repository import ParticipantRepository, SqliteParticipantRepository 
from vplaylist.repositories.playlist_repository import PlaylistRepository, SqlitePlaylistRepository 

def config_app():
    app = App()
    app.set(Player, PlayerVLC())
    app.set(AccountRepository, SqliteAccountRepository())
    app.set(AnalyticsRepository, SqliteAnalyticsRepository())
    app.set(ParticipantRepository, SqliteParticipantRepository())
    app.set(PlaylistRepository, SqlitePlaylistRepository())

if __name__ == '__main__':
    config_app()
    Cli()
