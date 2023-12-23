from abc import ABC
from typing import TypeVar, cast

from vplaylist.services.player import Player, PlayerVLC
from vplaylist.utils.singleton import Singleton


class _ServiceContainer:
    """
    Service Container pattern
    """

    def __init__(self) -> None:
        self.container: dict[type[ABC], ABC] = {}

    def get(self, interface: type[ABC]) -> ABC:
        return self.container[interface]

    def set(self, interface: type[ABC], instance: ABC) -> None:
        if not issubclass(type(instance), interface):
            raise Exception("Unable to set instance from this interface")
        self.container[interface] = instance


class App(metaclass=Singleton):
    def __init__(self) -> None:
        self._service_container = _ServiceContainer()
        self._service_container.set(Player, PlayerVLC())

    def app(self, name: type[ABC]) -> ABC:
        return self._service_container.get(name)


T = TypeVar("T", bound=ABC)


def app(interface: type[T]) -> T:
    concrete_class: T = cast(T, App().app(interface))
    return concrete_class
