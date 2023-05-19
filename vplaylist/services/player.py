import subprocess
from abc import ABC, abstractmethod
from typing import IO, AnyStr

# TODO instead of type ignore, may create our own stub
# file
import mpv  # type: ignore


class Player(ABC):
    @abstractmethod
    def __init__(self, playlist: IO[AnyStr]) -> None:
        pass

    @abstractmethod
    def launch_playlist(self) -> None:
        pass


class PlayerMPV:
    def __init__(self, playlist: IO[str]) -> None:
        self.player = mpv.MPV(
            log_handler=self.log_handler,
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            hwdec="auto",
        )

        self._init_key_press()
        self._init_events()
        self.player.loadlist(playlist.name)

    def log_handler(self, loglevel: str, component: str, message: str) -> None:
        print(f"[{loglevel}] {component}: {message}")

    def _init_key_press(self) -> None:
        # TODO maybe events to handle
        # things in database (add infos
        # on the fly etc. ?)
        @self.player.on_key_press("WHEEL_UP")  # type: ignore
        def wheel_up_binding() -> None:
            self.player.volume += 2
            print(self.player.volume)

        @self.player.on_key_press("WHEEL_DOWN")  # type: ignore
        def wheel_down_binding() -> None:
            self.player.volume -= 2
            print(self.player.volume)

        @self.player.on_key_press(">")  # type: ignore
        def right_arrow_pressed() -> None:
            self.player.playlist_next()

        @self.player.on_key_press("<")  # type: ignore
        def left_arrow_pressed() -> None:
            self.player.playlist_prev()

        @self.player.on_key_press("l")  # type: ignore
        def l_pressed() -> None:
            self.player.seek(10)

        @self.player.on_key_press("j")  # type: ignore
        def j_pressed() -> None:
            self.player.seek(-10)

    def _init_events(self) -> None:
        # TODO make an event
        # to know if a video is read
        # (if there is a playing of the same
        # video for a given time, we consider the
        # file as read, and put that in the database)
        pass

    def launch_playlist(self) -> None:
        while True:
            try:
                self.player.wait_for_playback()
            except mpv.ShutdownError:
                break
            except Exception:
                del self.player
                exit(1)

    def __del__(self) -> None:
        del self.player


class PlayerVLC:
    def __init__(self, playlist: IO[str]) -> None:
        self.playlist: IO[str] = playlist

    def launch_playlist(self) -> None:
        subprocess.run(["vlc", self.playlist.name])
