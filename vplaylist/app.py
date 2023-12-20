from collections.abc import Mapping
from vplaylist.config.config_registry import ConfigRegistry
from vplaylist.services.player import Player, PlayerVLC
from vplaylist.utils.singleton import Singleton

class _ServiceContainer:
    """
    Service Container pattern
    """

    def __init__(self) -> None:
        self.container: Mapping[Protocol, object] = {}

    def get(self, name: str) -> object:
        return self.container[name]

    def set(self, name: str, instance: object) -> None:
        self.container[name] = instance


class App(metaclass=Singleton):
    def __init__(self):
        self._service_container = _ServiceContainer()
        self._service_container.set(Player, PlayerVLC())

    def app(self, name: str) -> object:
        return self._service_container.get(name)

