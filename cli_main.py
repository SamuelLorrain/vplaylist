from vplaylist.adapter.cli.cli import Cli
from vplaylist.app import App

from vplaylist.services.player import Player, PlayerVLC


def config_app():
    app = App()
    app.set(Player, PlayerVLC())

if __name__ == '__main__':
    config_app()
    Cli()
