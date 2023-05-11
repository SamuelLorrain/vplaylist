import mpv
import subprocess


class Player:
    def __init__(self, playlist):
        self.player = mpv.MPV(
            log_handler=self.logHandler,
            input_default_bindings=True,
            input_vo_keyboard=True,
            osc=True,
            hwdec="auto",
        )

        self._initKeyPress()
        self._initEvents()
        self.player.loadlist(playlist.name)

    def logHandler(self, loglevel, component, message):
        print(f"[{loglevel}] {component}: {message}")

    def _initKeyPress(self):
        # TODO maybe events to handle
        # things in database (add infos
        # on the fly etc. ?)
        @self.player.on_key_press("WHEEL_UP")
        def wheel_up_binding():
            self.player.volume += 2
            print(self.player.volume)

        @self.player.on_key_press("WHEEL_DOWN")
        def wheel_down_binding():
            self.player.volume -= 2
            print(self.player.volume)

        @self.player.on_key_press(">")
        def right_arrow_pressed():
            self.player.playlist_next()

        @self.player.on_key_press("<")
        def left_arrow_pressed():
            self.player.playlist_prev()

        @self.player.on_key_press("l")
        def l_pressed():
            self.player.seek(10)

        @self.player.on_key_press("j")
        def j_pressed():
            self.player.seek(-10)

    def _initEvents(self):
        # TODO make an event
        # to know if a video is read
        # (if there is a playing of the same
        # video for a given time, we consider the
        # file as read, and put that in the database)
        pass

    def launchPlaylist(self):
        while True:
            try:
                self.player.wait_for_playback()
            except mpv.ShutdownError:
                break
            except Exception:
                del self.player
                exit(1)

    def __del__(self):
        del self.player


class PlayerVLC:
    def __init__(self, playlist):
        self.playlist = playlist

    def launchPlaylist(self):
        subprocess.run(["vlc", self.playlist.name])
